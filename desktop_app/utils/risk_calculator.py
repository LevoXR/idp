"""Risk calculation and recommendation generation"""


def calculate_risk_score(answers):
    """Calculate risk score based on assessment answers"""
    score = 0
    
    # High risk symptoms (2 points each)
    if answers.get('fever') == 'yes':
        score += 2
    if answers.get('shortness_breath') == 'yes':
        score += 2
    if answers.get('loss_taste_smell') == 'yes':
        score += 2
    if answers.get('contact_positive') == 'yes':
        score += 2
    
    # Moderate risk symptoms (1 point each)
    if answers.get('cough') == 'yes':
        score += 1
    if answers.get('fatigue') == 'yes':
        score += 1
    if answers.get('travel_history') == 'yes':
        score += 1
    if answers.get('chronic_disease') == 'yes':
        score += 1
    
    # Lifestyle factors
    if answers.get('public_transport') == 'yes':
        score += 1
    
    # Household size risk (1 point if >4 people)
    try:
        household_size = int(answers.get('household_size', '0'))
        if household_size > 4:
            score += 1
    except (ValueError, TypeError):
        pass
    
    # Protective factors (reduce score)
    if answers.get('vaccinated') == 'yes':
        score -= 1
    if answers.get('mask_usage') == 'yes':
        score -= 1
    
    # Ensure score doesn't go below 0
    return max(0, score)


def generate_recommendations(risk_level, answers):
    """Generate recommendations based on risk level and answers"""
    recommendations = []
    
    if risk_level == "High":
        recommendations.append("⚠️ HIGH RISK DETECTED")
        recommendations.append("Please seek immediate medical attention.")
        recommendations.append("Contact your healthcare provider or visit the nearest hospital.")
        recommendations.append("Self-isolate immediately and avoid contact with others.")
        if answers.get('vaccinated') != 'yes':
            recommendations.append("Consider getting vaccinated as soon as possible.")
    elif risk_level == "Moderate":
        recommendations.append("⚠️ MODERATE RISK")
        recommendations.append("Monitor your symptoms closely.")
        recommendations.append("Consider consulting with a healthcare professional.")
        recommendations.append("Stay home and avoid unnecessary outdoor activities.")
        recommendations.append("Continue social distancing and wear a mask.")
        if answers.get('vaccinated') != 'yes':
            recommendations.append("Getting vaccinated can help reduce your risk.")
    else:
        recommendations.append("✅ LOW RISK")
        recommendations.append("Continue following health guidelines.")
        recommendations.append("Maintain good hygiene practices.")
        recommendations.append("Wear masks in public places.")
        recommendations.append("Maintain social distancing.")
        if answers.get('vaccinated') != 'yes':
            recommendations.append("Consider getting vaccinated to protect yourself further.")
        else:
            recommendations.append("Good job staying vaccinated! Continue following safety measures.")
    
    # Additional specific recommendations based on symptoms
    if answers.get('fever') == 'yes' or answers.get('cough') == 'yes':
        recommendations.append("Monitor your temperature regularly and stay hydrated.")
    
    if answers.get('chronic_disease') == 'yes':
        recommendations.append("Since you have chronic conditions, be extra careful and consult your doctor regularly.")
    
    return '\n'.join(recommendations)


