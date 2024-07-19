import pandas as pd

# Load datasets
users_df = pd.read_csv('users.csv')
questions_df = pd.read_csv('questions.csv')
responses_df = pd.read_csv('responses.csv')

# Display the dataframes
print("Users Dataframe:")
print(users_df)

print("\nQuestions Dataframe:")
print(questions_df)

print("\nResponses Dataframe:")
print(responses_df)

# Initialize user profiles
user_profiles = {}
for index, row in users_df.iterrows():
    user_profiles[row['user_id']] = {
        'name': row['name'],
        'email': row['email'],
        'initial_assessment_score': row['initial_assessment_score'],
        'profile_created_at': row['profile_created_at'],
        'responses': []
    }

# Add responses to user profiles
for index, row in responses_df.iterrows():
    user_profiles[row['user_id']]['responses'].append({
        'question_id': row['question_id'],
        'response': row['response'],
        'correct': row['correct'],
        'response_time': row['response_time']
    })

# Function to get next question based on user's performance
def get_next_question(user_id):
    user_data = user_profiles[user_id]
    correct_answers = sum([response['correct'] for response in user_data['responses']])
    total_questions = len(user_data['responses'])
    accuracy = correct_answers / total_questions if total_questions > 0 else 0

    print(f"User {user_id} Accuracy: {accuracy}")
    print(f"Correct Answers: {correct_answers}, Total Questions: {total_questions}")

    if accuracy > 0.75:
        difficulty_level = 'hard'
    elif accuracy > 0.5:
        difficulty_level = 'medium'
    else:
        difficulty_level = 'easy'

    print(f"Selected Difficulty Level: {difficulty_level}")

    available_questions = questions_df[(questions_df['difficulty_level'] == difficulty_level) & (questions_df['is_mcq'] == True)]
    print(f"Available Questions for User {user_id} at Difficulty Level {difficulty_level}:")
    print(available_questions)

    if not available_questions.empty:
        return available_questions.sample(1).to_dict(orient='records')[0]
    else:
        return {"message": "No available questions"}

# Example usage
user_id = 1
next_question = get_next_question(user_id)
print(f"\nNext question for user {user_id}:")
print(next_question)
