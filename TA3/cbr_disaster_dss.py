# Case Study 1: Disaster Response Decision Support System

import copy

case_base = [
    {
        "case_id": "CASE-001",
        "event_name": "Typhoon Ursula (2019)",
        "problem": {
            "disaster_type": "Typhoon",
            "wind_speed_kph": 195,
            "flood_risk": "High",
            "area_type": "Coastal & Urban",
            "affected_population": 12000
        },
        "solution": {
            "evacuation_strategy": "Mandatory preemptive evacuation 24 hours prior to landfall",
            "shelter_capacity_allocated": 12000,
            "relief_packs_prepared": 15000,
            "rescue_boats_deployed": 10,
            "medical_teams": 4
        }
    },
    {
        "case_id": "CASE-002",
        "event_name": "Typhoon Odette (2021)",
        "problem": {
            "disaster_type": "Typhoon",
            "wind_speed_kph": 250,
            "flood_risk": "High",
            "area_type": "Urban",
            "affected_population": 25000
        },
        "solution": {
            "evacuation_strategy": "Forced evacuation of flood-prone urban zones & storm surge areas",
            "shelter_capacity_allocated": 25000,
            "relief_packs_prepared": 32000,
            "rescue_boats_deployed": 20,
            "medical_teams": 8
        }
    },
    {
        "case_id": "CASE-003",
        "event_name": "Monsoon Urban Flood (2022)",
        "problem": {
            "disaster_type": "Flood",
            "wind_speed_kph": 60,
            "flood_risk": "High",
            "area_type": "Urban",
            "affected_population": 8000
        },
        "solution": {
            "evacuation_strategy": "Immediate vertical evacuation to multi-story public schools",
            "shelter_capacity_allocated": 8000,
            "relief_packs_prepared": 10000,
            "rescue_boats_deployed": 15,
            "medical_teams": 3
        }
    },
    {
        "case_id": "CASE-004",
        "event_name": "Mindanao Earthquake (2019)",
        "problem": {
            "disaster_type": "Earthquake",
            "wind_speed_kph": 0,
            "flood_risk": "Low",
            "area_type": "Urban",
            "affected_population": 15000
        },
        "solution": {
            "evacuation_strategy": "Open-field assembly, structural inspection, and tent city setup",
            "shelter_capacity_allocated": 15000,
            "relief_packs_prepared": 18000,
            "rescue_boats_deployed": 0,
            "medical_teams": 10
        }
    }
]

def calculate_similarity(new_problem, past_problem):
    weights = {
        "disaster_type": 0.35,
        "flood_risk": 0.25,
        "area_type": 0.15,
        "wind_speed_kph": 0.15,
        "affected_population": 0.10
    }

    score = 0.0

    if new_problem["disaster_type"].lower() == past_problem["disaster_type"].lower():
        score += weights["disaster_type"]

    if new_problem["flood_risk"].lower() == past_problem["flood_risk"].lower():
        score += weights["flood_risk"]

    if new_problem["area_type"].lower() in past_problem["area_type"].lower() or \
       past_problem["area_type"].lower() in new_problem["area_type"].lower():
        score += weights["area_type"]

    wind_diff = abs(new_problem["wind_speed_kph"] - past_problem["wind_speed_kph"])
    wind_sim = max(0.0, 1.0 - (wind_diff / 300.0))
    score += weights["wind_speed_kph"] * wind_sim

    pop_diff = abs(new_problem["affected_population"] - past_problem["affected_population"])
    pop_sim = max(0.0, 1.0 - (pop_diff / 50000.0))
    score += weights["affected_population"] * pop_sim

    return round(score * 100, 2)


def retrieve_most_similar_case(new_problem, cases):
    ranked_cases = []
    for case in cases:
        sim_score = calculate_similarity(new_problem, case["problem"])
        ranked_cases.append((sim_score, case))

    ranked_cases.sort(key=lambda x: x[0], reverse=True)
    return ranked_cases


def adapt_solution(new_problem, retrieved_case):
    old_problem = retrieved_case["problem"]
    adapted_solution = copy.deepcopy(retrieved_case["solution"])

    pop_ratio = new_problem["affected_population"] / old_problem["affected_population"]

    adapted_solution["shelter_capacity_allocated"] = new_problem["affected_population"]
    adapted_solution["relief_packs_prepared"] = int(new_problem["affected_population"] * 1.25)
    adapted_solution["rescue_boats_deployed"] = max(
        1, int(round(adapted_solution["rescue_boats_deployed"] * pop_ratio))
    )
    adapted_solution["medical_teams"] = max(
        1, int(round(adapted_solution["medical_teams"] * pop_ratio))
    )

    if new_problem["flood_risk"].lower() == "high" and "urban" in new_problem["area_type"].lower():
        adapted_solution["evacuation_strategy"] = (
            f"{adapted_solution['evacuation_strategy']} + "
            "Activate high-rise urban vertical shelters & deploy water pumping stations"
        )

    return adapted_solution


def retain_new_case(new_event_name, new_problem, adapted_solution, cases):
    new_case_id = f"CASE-00{len(cases) + 1}"
    new_case_entry = {
        "case_id": new_case_id,
        "event_name": new_event_name,
        "problem": new_problem,
        "solution": adapted_solution
    }
    cases.append(new_case_entry)
    return new_case_entry


if __name__ == "__main__":
    print("=" * 75)
    print("   DISASTER RESPONSE DECISION SUPPORT SYSTEM (CASE-BASED REASONING)")
    print("=" * 75)

    new_event_name = "Typhoon Kristine (Urban Flood Alert)"
    new_problem_scenario = {
        "disaster_type": "Typhoon",
        "wind_speed_kph": 220,
        "flood_risk": "High",
        "area_type": "Urban",
        "affected_population": 30000
    }

    print("\n[1] NEW PROBLEM SCENARIO RECEIVED:")
    print(f"    Event Name          : {new_event_name}")
    for key, val in new_problem_scenario.items():
        print(f"    {key.replace('_', ' ').title():<20}: {val}")

    print("\n" + "-" * 75)
    print("[2] SIMILARITY ASSESSMENT & CASE RETRIEVAL:")
    ranked_results = retrieve_most_similar_case(new_problem_scenario, case_base)

    for score, case in ranked_results:
        print(f"    -> {case['case_id']} ({case['event_name']:<26}) | Similarity Score: {score}%")

    best_score, best_case = ranked_results[0]
    print(f"\n    [✔] MOST RELEVANT PAST CASE RETRIEVED:")
    print(f"        Case ID    : {best_case['case_id']} - {best_case['event_name']} ({best_score}% Match)")
    print(f"        Past Input : {best_case['problem']}")
    print(f"        Past Plan  : {best_case['solution']}")

    print("\n" + "-" * 75)
    print("[3] SOLUTION ADAPTATION (REUSE & REVISE):")
    final_solution = adapt_solution(new_problem_scenario, best_case)
    print(f"    Adapting '{best_case['event_name']}' solution for {new_problem_scenario['affected_population']} residents...")
    for key, val in final_solution.items():
        print(f"    * {key.replace('_', ' ').title():<28}: {val}")

    print("\n" + "-" * 75)
    print("[4] RETAIN STAGE (SYSTEM LEARNING):")
    saved_case = retain_new_case(new_event_name, new_problem_scenario, final_solution, case_base)
    print(f"    [✔] New case saved successfully as {saved_case['case_id']} ({saved_case['event_name']})!")

    print("\n    UPDATED CASE BASE SUMMARY (Total Cases: " + str(len(case_base)) + "):")
    for c in case_base:
        print(f"    - {c['case_id']}: {c['event_name']} "
              f"(Type: {c['problem']['disaster_type']}, Pop: {c['problem']['affected_population']})")
    print("=" * 75)