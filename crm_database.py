import pyodbc
import pandas as pd
from datetime import datetime, timedelta
from config import Config

class CRMDatabase:
    def __init__(self):
        """Инициализация подключения к базе данных CRM."""
        self.conn = pyodbc.connect(
            f'DRIVER={{SQL Server}};'
            f'SERVER={Config.CRM_SERVER};'
            f'DATABASE={Config.CRM_DATABASE};'
            f'UID={Config.CRM_USERNAME};'
            f'PWD={Config.CRM_PASSWORD}'
        )
        self.cursor = self.conn.cursor()

    def get_schedule(self, date=None, class_type=None):
        """Получение расписания занятий."""
        if date is None:
            date = datetime.now().date()
        
        query = """
        SELECT 
            c.ClassName,
            c.StartTime,
            c.EndTime,
            t.TrainerName,
            r.RoomName,
            c.MaxCapacity,
            (SELECT COUNT(*) FROM ClassBookings cb WHERE cb.ClassID = c.ClassID) as CurrentBookings
        FROM Classes c
        JOIN Trainers t ON c.TrainerID = t.TrainerID
        JOIN Rooms r ON c.RoomID = r.RoomID
        WHERE CAST(c.StartTime AS DATE) = ?
        """
        params = [date]
        
        if class_type:
            query += " AND c.ClassName LIKE ?"
            params.append(f'%{class_type}%')
            
        query += " ORDER BY c.StartTime"
        
        return pd.read_sql(query, self.conn, params=params)

    def get_client_info(self, phone_number):
        """Получение информации о клиенте."""
        query = """
        SELECT 
            c.ClientID,
            c.FirstName,
            c.LastName,
            c.PhoneNumber,
            m.MembershipType,
            m.ExpiryDate,
            m.RemainingClasses
        FROM Clients c
        LEFT JOIN Memberships m ON c.ClientID = m.ClientID
        WHERE c.PhoneNumber = ?
        """
        return pd.read_sql(query, self.conn, params=[phone_number])

    def get_studio_rules(self):
        """Получение правил студии."""
        query = """
        SELECT RuleCategory, RuleDescription
        FROM StudioRules
        ORDER BY RuleCategory, RuleID
        """
        return pd.read_sql(query, self.conn)

    def get_available_classes(self, date=None):
        """Получение доступных для записи занятий."""
        if date is None:
            date = datetime.now().date()
            
        query = """
        SELECT 
            c.ClassName,
            c.StartTime,
            c.EndTime,
            t.TrainerName,
            r.RoomName,
            c.MaxCapacity - (SELECT COUNT(*) FROM ClassBookings cb WHERE cb.ClassID = c.ClassID) as AvailableSpots
        FROM Classes c
        JOIN Trainers t ON c.TrainerID = t.TrainerID
        JOIN Rooms r ON c.RoomID = r.RoomID
        WHERE CAST(c.StartTime AS DATE) = ?
        AND c.StartTime > GETDATE()
        AND c.MaxCapacity > (SELECT COUNT(*) FROM ClassBookings cb WHERE cb.ClassID = c.ClassID)
        ORDER BY c.StartTime
        """
        return pd.read_sql(query, self.conn, params=[date])

    def close(self):
        """Закрытие соединения с базой данных."""
        self.cursor.close()
        self.conn.close() 