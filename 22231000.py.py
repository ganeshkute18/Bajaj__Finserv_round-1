import pandas as pd
import re

def find_absence_streaks(attendance_df):
    absence_streaks = []
    
    for student_id, group in attendance_df.groupby('student_id'):
        group = group.sort_values(by='attendance_date')
        streak_start = None
        streak_count = 0
        last_date = None
        
        for index, row in group.iterrows():
            if row['status'] == 'Absent':
                if streak_start is None:
                    streak_start = row['attendance_date']
                streak_count += 1
                last_date = row['attendance_date']
            else:
                if streak_count > 3:
                    absence_streaks.append([student_id, streak_start, last_date, streak_count])
                streak_start = None
                streak_count = 0
        
        if streak_count > 3:
            absence_streaks.append([student_id, streak_start, last_date, streak_count])
    
    return pd.DataFrame(absence_streaks, columns=['student_id', 'absence_start_date', 'absence_end_date', 'total_absent_days'])

def is_valid_email(email):
    pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*@[a-zA-Z]+\.com$'
    return bool(re.match(pattern, email))

def run():
    attendance_data = {
        'student_id': [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3],
        'attendance_date': pd.to_datetime([
            '2025-03-20', '2025-03-21', '2025-03-22', '2025-03-23', '2025-03-24',
            '2025-03-18', '2025-03-19', '2025-03-20', '2025-03-21', '2025-03-22',
            '2025-03-15', '2025-03-16', '2025-03-17'
        ]),
        'status': ['Present', 'Absent', 'Absent', 'Absent', 'Absent', 'Absent', 'Absent', 'Absent', 'Present', 'Absent', 'Present', 'Absent', 'Absent']
    }
    
    students_data = {
        'student_id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie'],
        'parent_email': ['alice_parent@gmail.com', 'bob.parent@outlook.com', 'charlie_123@invalid']
    }
    
    attendance_df = pd.DataFrame(attendance_data)
    students_df = pd.DataFrame(students_data)
    
    absence_streaks_df = find_absence_streaks(attendance_df)
    result_df = absence_streaks_df.merge(students_df, on='student_id', how='left')
    
    result_df['email'] = result_df['parent_email'].apply(lambda x: x if is_valid_email(x) else None)
    result_df['msg'] = result_df.apply(
        lambda row: f"Dear Parent, your child {row['name']} was absent from {row['absence_start_date'].date()} to {row['absence_end_date'].date()} for {row['total_absent_days']} days. Please ensure their attendance improves."
        if row['email'] else None, axis=1
    )
    
    final_df = result_df[['student_id', 'absence_start_date', 'absence_end_date', 'total_absent_days', 'email', 'msg']]
    
    print("\n" + "="*50)
    print("Final Output")
    print("="*50 + "\n")
    print(final_df.to_string(index=False))
    print("\n" + "="*50)
    
    return final_df

df_output = run()
