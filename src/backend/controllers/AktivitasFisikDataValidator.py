import re

datetime_regex = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"
class ActivityValidator:
    @staticmethod
    def validate_log_id(log_id):
        if not isinstance(log_id, int) or log_id <= 0:
            raise ValueError("Usia harus berupa angka positif.")
    
    @staticmethod
    def validate_tinggi(date):
        if isinstance(date, str):
            if re.match(datetime_regex, sample_datetime):
                try:
                # Validate using datetime module
                    valid_datetime = datetime.strptime(sample_datetime, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    print("Invalid datetime value.")
            else:
                print("Does not match format.")
        else:
            raise ValueError("Bukan string")
    
    @staticmethod
    def validate_activity_id(activity_id):
        if not isinstance(activity_id, int) or activity_id <= 0:
            raise ValueError("Id Tidak Valid")
    
    @staticmethod
    def validate_achievement(achievement):
        if not isinstance(achievement, int) or achievement <= 0:
            raise ValueError("Data Tidak Valid")
        
    @staticmethod
    def validate_calorie(calorie):
        if not isinstance(calorie, int) or calorie <= 0:
            raise ValueError("Data Tidak Valid")
