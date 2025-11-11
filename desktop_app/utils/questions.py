"""Assessment questions for the health questionnaire"""


def get_assessment_questions():
    """Get list of assessment questions"""
    return [
        {'id': 'fever', 'question': 'Do you have a fever (temperature above 38°C or 100.4°F)?', 'type': 'yes_no'},
        {'id': 'cough', 'question': 'Do you have a cough or sore throat?', 'type': 'yes_no'},
        {'id': 'shortness_breath', 'question': 'Do you experience shortness of breath or difficulty breathing?', 'type': 'yes_no'},
        {'id': 'fatigue', 'question': 'Do you have unusual fatigue or body aches?', 'type': 'yes_no'},
        {'id': 'loss_taste_smell', 'question': 'Have you experienced loss of taste or smell?', 'type': 'yes_no'},
        {'id': 'travel_history', 'question': 'Have you traveled outside your state in the past 14 days?', 'type': 'yes_no'},
        {'id': 'contact_positive', 'question': 'Have you been in close contact with someone who tested positive for COVID-19?', 'type': 'yes_no'},
        {'id': 'public_transport', 'question': 'Do you use public transportation regularly?', 'type': 'yes_no'},
        {'id': 'chronic_disease', 'question': 'Do you have any chronic medical conditions (diabetes, heart disease, respiratory issues)?', 'type': 'yes_no'},
        {'id': 'household_size', 'question': 'How many people live in your household?', 'type': 'numeric'},
        {'id': 'mask_usage', 'question': 'Do you always wear a mask when outside?', 'type': 'yes_no'},
        {'id': 'vaccinated', 'question': 'Have you been vaccinated against COVID-19?', 'type': 'yes_no'},
    ]


