from pydantic import BaseModel

class EnumLib(BaseModel):
    flags: dict[str, list[str]]

flags = {
    "Attendance.AttendanceBonusPolicy" : [
        """
        Table: Attendance.AttendanceBonusPolicy        
        Field: AttendanceFlags
        Flags:
            1 -> Absent, 
            2 -> Extreme Delay, 
            3 -> Delay, 
            4 -> Visit, 
            5 -> Present, 
            6 -> Leave, 
            61 -> Leave 1st Half, 
            62 -> Leave 2nd Half, 
            9 -> Hourly Leave, 
            7 -> Holiday, 
            8 -> Weekend,
        """
    ],
    "Attendance.AttendancePolicyDetails" : [
        """
        Table: Attendance.AttendancePolicyDetails
        Field: WorkingTypeId
        Flags:
            1 -> Full Day, 
            2 -> Half Day, 
            3 -> Weekend,
        """,
        """
        Table: Attendance.AttendancePolicyDetails
        Field: DayId
        Flags:
            1 -> Saturday, 
            2 -> Sunday, 
            3 -> Monday, 
            4 -> Tuesday, 
            5 -> Wednesday, 
            6 -> Thursday, 
            7 -> Friday
        """
    ],
    "Attendance.AttendanceReconciliation": [
    """
    Table: Attendance.AttendanceReconciliation
    Field: ApprovalStatus
    Flags:
        1 -> Pending, 
        2 -> Approved, 
        3 -> Rejected
    """
    ],
    "Attendance.CompensatedExtraTime": [
    """
    Table: Attendance.CompensatedExtraTime
    Field: CompensatedFromId
    Flags:
        1 -> No, 
        2 -> With Salary, 
        3 -> With Leave
    """
    ],
    "Attendance.DeletedAttendance": [
    """
    Table: Attendance.DeletedAttendance
    Field: EmployeeTypeId
    Flags:
        0 -> All, 
        1 -> General, 
        2 -> Roster
    """    
    ],
    "Attendance.MultipleCheckInOut": [
    """
    Table: Attendance.MultipleCheckInOut    
    Field: CheckingType
    Flags:
        1 -> Check In, 
        2 -> Check Out
    """
    ],
    "Attendance.SalaryOrLeaveDeduction": [
    """
    Table: Attendance.SalaryOrLeaveDeduction
    Field: AbsentOrDelayTypeId
    Flags:
        1 -> Absent, 
        2 -> Delay, 
        3 -> Extreme Delay, 
        4 -> Underwork, 
        5 -> Unpaid Leave, 
        6 -> Early Out
    """,
    """
    Table: Attendance.SalaryOrLeaveDeduction
    Field: AbsentOrDelayDeductionTypeId
    Flags:
        1 -> Salary, 
        2 -> Leave
    """
    ],
    "Attendance.TimeSlotBasedOvertimePolicy" : [
    """
    Table: Attendance.TimeSlotBasedOvertimePolicy
    Field: ApplicableAttendanceFlagIds
    Flags:
        1 -> Weekend, 
        2 -> Holiday, 
        3 -> Full Day Leave, 
        4 -> First Half Leave, 
        5 -> Second Half Leave, 
        6 -> Visit, 
        7 -> Working Day, 
        8 -> Half Working Day, 
        9 -> Absent, 
        10 -> Hourly Leave
    """
    ],
    "Attendance.ProcessEligibleEmployee": [
    """
    Table: Attendance.ProcessEligibleEmployee
    Field: EligibleEmployeeOperationTypeId
    Flags:
        1 -> Attendance, 
        2 -> Bonus, 
        3 -> HRD, 
        4 -> Increment, 
        5 -> Leave, 
        6 -> Pay, 
        7 -> PF, 
        8 -> Tax
    """
    ],
    "Attendance.ProcessEligibleEmployee": [
    """
    Table: Attendance.ProcessEligibleEmployee
    Field: EligibleEmployeeConditionTypes
    Flags:
        1 -> Job Status, 
        2 -> Job Base
    """
    ],
    "Attendance.ApprovalWorkFlowMapping": [
    """
    Table: Attendance.ApprovalWorkFlowMapping
    Field: ApplicationType
    Flags:
        1 -> Leave Application, 
        2 -> Visit Application, 
        3 -> Claim, 
        4 -> Advance Salary
    """
    ],
    "Leave.Applicationstate" : [
    """
    Table: Leave.Applicationstate
    Field: CurrentApplicationState
    Flags:
        1 -> Under Processing, 
        2 -> Approved, 
        3 -> Rejected, 
        4 -> Recommended, 
        5 -> Cancelled, 
        6 -> Reliever Processing, 
        7 -> Modified & Approved, 
        8 -> Modified & Under Processing
    """
    ]
}
    
enum_lib = EnumLib(flags=flags)

def get_neccessary_flags(table_names: list[str]) -> list[str]:
    neccessary_flags = []
    for table_name in table_names:
        if table_name in enum_lib.flags:
            neccessary_flags.extend(enum_lib.flags[table_name])
    return neccessary_flags

# print(get_neccessary_flags(["Attendance.AttendancePolicyDetails"]))