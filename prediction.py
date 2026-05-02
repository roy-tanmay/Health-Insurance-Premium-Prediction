import pandas as pd
import joblib
import warnings as wr
wr.filterwarnings("ignore")

# loading Artifacts
def load_artifacts():
    model_young     = joblib.load("files/model_young.joblib")
    model_rest      = joblib.load("files/model_rest.joblib")
    scaler_young    = joblib.load("files/scaler_young.joblib")
    scaler_rest     = joblib.load("files/scaler_rest.joblib")
    columns         = joblib.load("files/columns.joblib")
    return model_young, model_rest, scaler_young, scaler_rest, columns


# Configuring the categorical columns
Insurance_map   = {"Bronze": 1, "Silver": 2, "Gold":3 }
Region_map      = {"Northwest":"region_Northwest",
                    "Southeast":"region_Southeast",
                    "Southwest":"region_Southwest"}
BMI_map         = {"Obesity":"bmi_category_Obesity",
                    "Overweight":"bmi_category_Overweight",
                    "Underweight":"bmi_category_Underweight"}
Smoking_map     = {"Occasional":"smoking_status_Occasional",
                    "Regular":"smoking_status_Regular"}
Employment_map  = {"Salaried":"employment_status_Salaried",
                    "Self-Employed":"employment_status_Self-Employed"}

# Manually assign values for each categorical & numerical input, based on user_data
def build_user_input_df(data:dict, columns):
    row = {col:0 for col in columns}

    row['age'] = data['age']
    row['number_of_dependants'] = data['number_of_dependants']
    row['income_lakhs'] = data['income_lakhs']
    row['insurance_plan'] = Insurance_map[data['insurance_plan']]
    row['genetical_risk'] = data['genetical_risk']
    row['normalized_risk_score'] = data['normalized_risk_score']

    if data['gender'] == 'Male':
        row['gender_Male'] = 1

    if data['region'] in Region_map:
        row[Region_map[data['region']]] = 1

    if data['marital_status'] == 'Unmarried':
        row['marital_status_Unmarried'] = 1

    if data['bmi_category'] in BMI_map:
        row[BMI_map[data['bmi_category']]] = 1

    if data['smoking_status'] in Smoking_map:
        row[Smoking_map[data['smoking_status']]] = 1

    if data['employment_status'] in Employment_map:
        row[Employment_map[data['employment_status']]] = 1

    return pd.DataFrame([row])[columns]

# Calculate Normalised Risk score
Risk_score = {
    "diabetes": 6,
    "heart disease": 8,
    "high blood pressure":6,
    "thyroid": 5,
    "no disease": 0,
    "none":0
}
def calculate_normalized_risk_score(medical_history: str):
    diseases = medical_history.lower().split("&")
    max_score = 14
    min_score = 0

    # Calculating total risk score and normalized risk score
    total_risk_score = sum(Risk_score.get(dis, 0) for dis in diseases)
    normalized_risk_score = (total_risk_score - min_score) / (max_score - min_score)
    return normalized_risk_score

# Scaling
def scaling_and_prediction(df:pd.DataFrame, scaler_dict: dict, model):
    scaled_df = df.copy()
    # Adding the 'income_level' column
    """
    To enable scaling for the column 'income_level', 
    which is present in cols_to_scale but not in the actual columns, 
    I need to add this column. After scaling, I will remove the column.
    """
    scaled_df['income_level'] = 0

    # Scale only the columns the scaler was trained on
    scale_cols = scaler_dict['cols_to_scale']
    scaled_df[scale_cols] = scaler_dict['scaler'].transform(scaled_df[scale_cols])

    # Dropping column ('income_level')
    scaled_df = scaled_df.drop('income_level', axis=1)

    # Prediction
    return model.predict(scaled_df)[0]

# Main prediction
def predicting_premium(data: dict ):
    model_young, model_rest, scaler_young, scaler_rest, columns = load_artifacts()
    user_data = data

    # Compute normalized risk score from medical history
    user_data['normalized_risk_score'] = calculate_normalized_risk_score(user_data['medical_history'])
    user_data.pop('medical_history')

    final_df = build_user_input_df(user_data, columns)

    if user_data['age'] < 25:
        return scaling_and_prediction(final_df, scaler_young, model_young)
    else:
        return scaling_and_prediction(final_df, scaler_rest, model_rest)












