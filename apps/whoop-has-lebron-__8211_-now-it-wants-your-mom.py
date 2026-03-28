```python
#!/usr/bin/env python3
"""
Whoop Mom Transition Demo: Simulates health wearable data analysis for
elite athletes vs. mainstream users, showing how metrics adapt to audience.
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

# Constants
ELITE_TARGETS = {
    'recovery_min': 70,  # Elite need high recovery
    'strain_max': 20.0,  # Elite tolerate high strain
    'sleep_target_min': 480,  # minutes
    'hrv_min': 80,  # ms
}

MAINSTREAM_TARGETS = {
    'recovery_min': 50,  # Lower bar for general health
    'strain_max': 10.0,  # Conservative for everyday folks
    'sleep_target_min': 420,  # 7 hours minimum
    'hrv_min': 60,  # ms
}

FDA_TRIGGERS = {
    'afib_threshold': 3,  # episodes per week triggers medical alert
    'bp_critical': 180,  # systolic triggers referral
    'resting_hr_critical': 120,  # bpm
}

def generate_user_data(user_type: str, days: int = 7) -> List[Dict]:
    """Simulate health metrics for a user type over N days."""
    data = []
    base_date = datetime.now() - timedelta(days=days)
    
    for i in range(days):
        date = (base_date + timedelta(days=i)).strftime('%Y-%m-%d')
        
        if user_type == 'elite':
            # Athlete: high strain, good recovery, optimized sleep
            strain = random.uniform(15.0, 22.0)
            recovery = random.uniform(65, 95)
            sleep = random.randint(420, 600)
            hrv = random.randint(70, 120)
            # Athletes rarely have medical alerts
            afib_episodes = random.choices([0, 1], weights=[0.95, 0.05])[0]
            bp_systolic = random.randint(110, 130)
        else:  # mainstream
            # Mom/dad: moderate strain, variable recovery, inconsistent sleep
            strain = random.uniform(3.0, 12.0)
            recovery = random.uniform(30, 80)
            sleep = random.randint(360, 540)
            hrv = random.randint(40, 90)
            # Mainstream may show occasional issues
            afib_episodes = random.choices([0, 1, 2], weights=[0.85, 0.10, 0.05])[0]
            bp_systolic = random.randint(115, 145)
        
        data.append({
            'date': date,
            'strain': round(strain, 1),
            'recovery': recovery,
            'sleep_minutes': sleep,
            'hrv_ms': hrv,
            'afib_episodes': afib_episodes,
            'bp_systolic': bp_systolic,
        })
    
    return data

def analyze_elite_profile(metrics: List[Dict]) -> Dict:
    """Analyze data using elite athlete framework."""
    insights = []
    alerts = []
    
    for day in metrics:
        rec = day['recovery']
        strain = day['strain']
        sleep = day['sleep_minutes']
        hrv = day['hrv_ms']
        
        # Elite-specific feedback
        if rec < ELITE_TARGETS['recovery_min'] and strain > ELITE_TARGETS['strain_max'] * 0.9:
            insights.append(f"{day['date']}: High strain with low recovery — risk of overtraining")
        if sleep < ELITE_TARGETS['sleep_target_min'] and strain > 15:
            insights.append(f"{day['date']}: Insufficient sleep for intense training day")
        if hrv < ELITE_TARGETS['hrv_min']:
            alerts.append(f"{day['date']}: HRV dropped — consider reducing intensity")
    
    return {
        'user_type': 'elite',
        'message': "Optimize for performance. Focus on recovery to match high strain.",
        'insights': insights[:3],  # Top 3
        'alerts': alerts,
        'compliance': 'ok'
    }

def analyze_mainstream_profile(metrics: List[Dict]) -> Dict:
    """Analyze data using mainstream wellness framework."""
    insights = []
    alerts = []
    medical_flags = []
    
    # Weekly aggregates
    avg_strain = sum(d['strain'] for d in metrics) / len(metrics)
    avg_recovery = sum(d['recovery'] for d in metrics) / len(metrics)
    low_sleep_days = sum(1 for d in metrics if d['sleep_minutes'] < MAINSTREAM_TARGETS['sleep_target_min'])
    total_afib = sum(d['afib_episodes'] for d in metrics)
    high_bp_days = sum(1 for d in metrics if d['bp_systolic'] > 140)
    
    if avg_strain < MAINSTREAM_TARGETS['strain_max'] * 0.5:
        insights.append("You're under-engaging — consider more daily movement")
    if low_sleep_days > 3:
        insights.append("Frequent short sleep — prioritize consistent bedtime")
    if avg_recovery < 50:
        insights.append("Recovery is low — focus on stress management and sleep")
    
    # Medical monitoring
    if total_afib >= FDA_TRIGGERS['afib_threshold']:
        medical_flags.append(f"Detected {total_afib} AFib episodes — consult a cardiologist")
    if high_bp_days >= 2:
        medical_flags.append("Multiple elevated blood pressure readings — schedule check-up")
    
    return {
        'user_type': 'mainstream',
        'message': "Build sustainable habits. Small improvements matter.",
        'insights': insights[:3],
        'alerts': alerts,
        'medical_flags': medical_flags,
        'compliance': 'review_needed' if medical_flags else 'ok'
    }

def check_fda_compliance(metrics: List[Dict]) -> Dict:
    """Check if user triggered any FDA-regulated medical device flags."""
    flags = []
    recommendations = []
    
    for day in metrics:
        if day['afib_episodes'] > 2:
            flags.append("AFib detection threshold exceeded — requires medical disclaimer")
        if day['bp_systolic'] > FDA_TRIGGERS['bp_critical']:
            flags.append("Critical blood pressure reading — emergency alert implied")
        if day['resting_hr_critical'] < 40 or day['resting_hr_critical'] > 120:
            flags.append("Abnormal resting heart rate — medical review needed")
    
    if flags:
        recommendations.append("Ensure FDA 510(k) clearance covers these metrics")
        recommendations.append("Display clear medical disclaimer in app")
    
    return {
        'fda_flags': flags,
        'recommendations': recommendations,
        'requires_clearance': len(flags) > 0
    }

def simulate_whoop_expansion():
    """Demonstrate how Whoop adapts analysis for different user types."""
    print("=" * 60)
    print("WHOOP MOM TRANSITION DEMO")
    print("Elite athlete vs. mainstream health analysis")
    print("=" * 60)
    
    # Generate sample data
    elite_data = generate_user_data('elite', days=7)
    mom_data = generate_user_data('mainstream', days=7)
    
    # Analyze each profile
    elite_analysis = analyze_elite_profile(elite_data)
    mom_analysis = analyze_mainstream_profile(mom_data)
    
    # Check regulatory compliance
    fda_check = check_fda_compliance(mom_data)  # Mainstream triggers more flags
    
    # Display results
    print("\n--- ELITE ATHLETE METRICS ---")
    print(f"Profile: {elite_analysis['user_type'].upper()}")
    print(f"Summary: {elite_analysis['message']}")
    if elite_analysis['insights']:
        print("Top insights:")
        for i, insight in enumerate(elite_analysis['insights'], 1):
            print(f"  {i}. {insight}")
    else:
        print("  No critical insights — performance on track")
    
    print("\n--- MAINSTREAM (MOM) METRICS ---")
    print(f"Profile: {mom_analysis['user_type'].upper()}")
    print(f"Summary: {mom_analysis['message']}")
    if mom_analysis['insights']:
        print("Wellness insights:")
        for i, insight in enumerate(mom_analysis['insights'], 1):
            print(f"  {i}. {insight}")
    if mom_analysis['medical_flags']:
        print("Medical alerts:")
        for flag in mom_analysis['medical_flags']:
            print(f"  ! {flag}")
    
    print("\n--- FDA COMPLIANCE CHECK ---")
    if fda_check['fda_flags']:
        print("FLAGS DETECTED:")
        for flag in fda_check['fda_flags']:
            print(f"  * {flag}")
        print("\nRequired actions:")
        for rec in fda_check['recommendations']:
            print(f"  - {rec}")
    else:
        print("No medical device triggers met. Consumer wellness mode compliant.")
    
    print("\n--- BUSINESS IMPACT ---")
    print("Elite users: Focus on performance optimization, coach integration.")
    print("Mainstream users: Health insights + medical alerts drive engagement,")
    print("                 but require FDA clearance for diagnostic claims.")
    print("\nWhoop's challenge: Serve both without diluting the brand or")
    print("triggering unnecessary regulation. Premium subscription ($30/mo).")
    print("=" * 60)

if __name__ == "__main__":
    simulate_whoop_expansion()
```