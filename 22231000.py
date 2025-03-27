import pandas as pd

file_path = "C:\Downloads\Data Engineering\Data Engineering\data - sample.xlsx"  
df_attendance = pd.read_excel(file_path, sheet_name="Attendance_data")

df_attendance["attendance_date"] = pd.to_datetime(df_attendance["attendance_date"], dayfirst=True)

df_absent = df_attendance[df_attendance["status"] == "Absent"].sort_values(["student_id", "attendance_date"])

def get_latest_absence_streak(df):
    latest_listt = []
    for student_id, group in df.groupby("student_id"):
        sorted_dates = group["attendance_date"].tolist()
        
        listt = []
        start_date = sorted_dates[0]
        prev_date = start_date
        count = 1

        for i in range(1, len(sorted_dates)):
            if (sorted_dates[i] - prev_date).days == 1:
                count += 1
            else:
                if count > 3: 
                    listt.append((start_date, prev_date, count))
                start_date = sorted_dates[i]
                count = 1
            prev_date = sorted_dates[i]
        
        if count > 3:
            listt.append((start_date, prev_date, count))
        
        if listt:
            latest_streak = max(listt, key=lambda x: x[1])
            latest_listt.append((student_id, latest_streak[0], latest_streak[1], latest_streak[2]))
    
    return pd.DataFrame(latest_listt, columns=["student_id", "absence_start_date", "absence_end_date", "total_absent_days"])

df_absence_listt = get_latest_absence_streak(df_absent)

output_file = "C:\Downloads\Data Engineering\Data Engineering\data - sample.xlsx"
df_absence_listt.to_excel(output_file, index=False)

print(df_absence_listt)

