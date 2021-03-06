from __future__ import annotations

from typing import TYPE_CHECKING, overload

from flask_login import UserMixin

from sqlalchemy import (
    Column,
    ForeignKey,
    UniqueConstraint,
    Integer,
    VARCHAR,
    Text,
    Date,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..extensions import db

if TYPE_CHECKING:
    from typing import Iterable, List, Tuple, Optional, Union
    from flask_sqlalchemy import BaseQuery
    from datetime import date
    from . import Subject, Class, Log, Exam, ClassCc


"""ASSOCIATION TABLES"""


class ParentStudents(db.Model):
    __tablename__ = "parent_students"

    query: BaseQuery

    id = Column(Integer, primary_key=True)

    # Foreign Key
    parent_id = Column(Integer, ForeignKey("parent.id"))
    student_id = Column(Integer, ForeignKey("student.id"))


"""CONSTANT TABLES"""


class Department(db.Model):
    __tablename__ = "department"

    query: BaseQuery

    id = Column(Integer, primary_key=True)
    full_name = Column(Text, unique=True)
    short_name = Column(Text, unique=True)

    # Relationships
    students: List[Student] = relationship("Student", back_populates="dept")
    staffs: List[Staff] = relationship("Staff", back_populates="dept")

    # External Relationships
    subjects: List[Subject] = relationship(
        "SubjectDepartment", back_populates="department"
    )
    classes: List[Class] = relationship(
        "Class", secondary="class_dept", back_populates="departments"
    )

    def __init__(self, full_name: str, short_name: str) -> None:
        self.full_name = full_name
        self.short_name = short_name

    def __repr__(self) -> str:
        return f"<Department: {self.short_name}>"


class Designation(db.Model):
    __tablename__ = "designation"

    query: BaseQuery

    id = Column(Integer, primary_key=True)
    full_name = Column(Text, unique=True)
    short_name = Column(Text, unique=True)

    # Relationships
    staffs: List[Staff] = relationship("Staff", back_populates="designation")

    def __init__(self, full_name: str, short_name: str) -> None:
        self.full_name = full_name
        self.short_name = short_name

    def __repr__(self) -> str:
        return f"<Designation: {self.full_name}>"


class BloodGroup(db.Model):
    __tablename__ = "blood_group"

    query: BaseQuery

    id = Column(Integer, primary_key=True)
    blood_group = Column(Text, unique=True)

    # Relationships
    students: List[Student] = relationship("Student", back_populates="blood_grp")
    staffs: List[Staff] = relationship("Staff", back_populates="blood_grp")

    def __init__(self, blood_group: str) -> None:
        self.blood_group = blood_group

    def __repr__(self) -> str:
        return f"<BloodGroup: {self.blood_group}>"


class Role(db.Model):
    __tablename__ = "role"

    query: BaseQuery

    id = Column(Integer, primary_key=True)
    role_name = Column(Text, unique=True)

    # Relationships
    users: List[User] = relationship("User", back_populates="role")

    def __init__(self, role_name: str) -> None:
        self.role_name = role_name

    def __repr__(self) -> str:
        return f"<Role: {self.role_name}>"


class Calendar(db.Model):
    __tablename__ = "calendar"

    query: BaseQuery

    id = Column(Integer, primary_key=True)
    date_ = Column(Date, unique=True)
    is_govt_holiday = Column(Boolean)
    holiday_rsn = Column(Text)

    # Relationship
    classes: List[Class] = relationship("ClassCalendar", back_populates="date_")
    logs: List[Log] = relationship("Log", back_populates="date_")
    exams: List[Exam] = relationship("Exam", back_populates="date_")

    def __init__(
        self,
        date_: date,
        is_govt_holiday: Optional[bool] = False,
        holiday_rsn: Optional[str] = None,
    ) -> None:
        self.date_ = date_
        self.is_govt_holiday = is_govt_holiday
        self.holiday_rsn = holiday_rsn

    def __repr__(self) -> str:
        return f"<Calendar: {self.date.strftime('%d-%m-%Y')} - {'Holiday' if self.is_govt_holiday == True else 'Working Day' }>"


class NotificationCategory(db.Model):
    __tablename__ = "notification_category"

    query: BaseQuery

    id = Column(Integer, primary_key=True)
    category = Column(VARCHAR(20))

    # Relationships
    notifications: List[Notification] = relationship(
        "Notification", back_populates="category"
    )

    def __init__(self, category: str) -> None:
        self.category = category

    def __repr__(self) -> str:
        return f"<NotificationCategory: {self.category}>"


"""PERSON TABLES"""


class Admin(db.Model):
    __tablename__ = "admin"

    query: BaseQuery

    id = Column(Integer, primary_key=True)
    is_staff = Column(Boolean)
    f_name = Column(Text)
    m_name = Column(Text, nullable=True)
    l_name = Column(Text)

    # Foreign Key
    staff_id = Column(Integer, ForeignKey("staff.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"))

    # Relationships
    staff: Staff = relationship("Staff", back_populates="admin")
    user: User = relationship("User")

    @overload
    def __init__(self, staff: Staff, user: User) -> None:
        ...

    @overload
    def __init__(
        self, f_name: str, l_name: str, user: User, m_name: Optional[str]
    ) -> None:
        ...

    def __init__(self, **kwargs: Union[str, Staff]) -> None:
        self.f_name = kwargs.get("f_name")
        self.m_name = kwargs.get("m_name")
        self.l_name = kwargs.get("l_name")
        self.staff = kwargs.get("staff")
        self.is_staff = False if kwargs.get("staff") == None else True
        self.user = kwargs.get("user")

    def __repr__(self) -> str:
        if self.is_staff is True:
            return f"<Admin: {self.staff}>"
        else:
            return f"<Admin: {self.f_name} {self.l_name}>"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Staff(db.Model):
    __tablename__ = "staff"

    query: BaseQuery

    id = Column(Integer, primary_key=True)

    # Data Fields
    f_name = Column(Text)
    m_name = Column(Text, nullable=True)
    l_name = Column(Text)
    staff_id = Column(Text)
    m_no = Column(Text)
    date_of_joining = Column(Date)
    is_cc = Column(Boolean)
    is_admin = Column(Boolean)
    is_active_staff = Column(Boolean)

    # Foreign Keys
    dept_id = Column(Integer, ForeignKey("department.id"))
    desig_id = Column(Integer, ForeignKey("designation.id"))
    blood_grp_id = Column(Integer, ForeignKey("blood_group.id"))
    user_id = Column(Integer, ForeignKey("user.id"))

    # Relationships
    dept: Department = relationship("Department", back_populates="staffs")
    designation: Designation = relationship("Designation", back_populates="staffs")
    blood_grp: BloodGroup = relationship("BloodGroup", back_populates="staffs")
    admin: Admin = relationship("Admin", back_populates="staff", uselist=False)
    user: User = relationship("User")
    subjects_handling: List[Subject] = relationship(
        "Subject", secondary="subject_staff", back_populates="staffs"
    )
    classes_as_cc: List[ClassCc] = relationship("ClassCc", back_populates="cc")
    logs: List[Log] = relationship("Log", back_populates="staff")

    def __init__(
        self,
        f_name: str,
        l_name: str,
        staff_id: str,
        dept: Department,
        designation: Designation,
        date_of_joining: date,
        m_no: str,
        blood_grp: BloodGroup,
        user: User,
        is_cc: Optional[bool] = False,
        is_active_staff: Optional[bool] = True,
        is_admin: Optional[bool] = False,
        m_name: Optional[str] = None,
    ) -> None:
        self.f_name = f_name
        self.m_name = m_name
        self.l_name = l_name
        self.staff_id = staff_id
        self.dept = dept
        self.designation = designation
        self.blood_grp = blood_grp
        self.m_no = m_no
        self.date_of_joining = date_of_joining
        self.is_cc = is_cc
        self.is_admin = is_admin
        self.is_active_staff = is_active_staff
        self.user = user

    def __repr__(self) -> str:
        return f"<Staff: {self.f_name} {self.l_name}, {self.dept.short_name} - {self.designation.short_name}>"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Student(db.Model):
    __tablename__ = "student"

    query: BaseQuery

    id = Column(Integer, primary_key=True)

    # Data Fields
    f_name = Column(Text)
    m_name = Column(Text, nullable=True)
    l_name = Column(Text)
    roll_no = Column(Integer, unique=True, nullable=True)
    batch = Column(Integer)
    library_id = Column(Text, unique=True, nullable=True)
    dob = Column(Date)
    regulation = Column(Integer)
    m_no = Column(Text)
    is_rep = Column(Boolean)
    is_active_stud = Column(Boolean)
    is_lateral_entry = Column(Boolean)
    is_alumni = Column(Boolean)

    # Foreign Keys
    dept_id = Column(Integer, ForeignKey("department.id"))
    class_id = Column(Integer, ForeignKey("class.id"))
    blood_grp_id = Column(Integer, ForeignKey("blood_group.id"))
    user_id = Column(Integer, ForeignKey("user.id"))

    # Relationships
    dept: Department = relationship("Department", back_populates="students")
    class_: Class = relationship("Class", back_populates="students")
    blood_grp: BloodGroup = relationship("BloodGroup", back_populates="students")
    user: User = relationship("User")
    parents: List[Parent] = relationship(
        "Parent", secondary="parent_students", back_populates="children"
    )

    class_as_rep: List[Class] = relationship("ClassRep", back_populates="rep")
    attendance: List[Log] = relationship("Attendance", back_populates="student")
    exams: List[Exam] = relationship("ExamStudent", back_populates="student")

    def __init__(
        self,
        f_name: str,
        l_name: str,
        batch: int,
        dob: date,
        regulation: int,
        m_no: str,
        dept: Department,
        blood_group: BloodGroup,
        class_: Class,
        user: User,
        is_lateral_entry: Optional[bool] = False,
        is_rep: Optional[bool] = False,
        is_active_stud: Optional[bool] = True,
        is_alumni: Optional[bool] = False,
        m_name: Optional[str] = None,
        roll_no: Optional[int] = None,
        library_id: Optional[str] = None,
    ):
        self.f_name = f_name
        self.m_name = m_name
        self.l_name = l_name
        self.roll_no = roll_no
        self.batch = batch
        self.library_id = library_id
        self.dob = dob
        self.regulation = regulation
        self.dept = dept
        self.blood_grp = blood_group
        self.class_ = class_
        self.m_no = m_no
        self.is_rep = is_rep
        self.is_active_stud = is_active_stud
        self.is_lateral_entry = is_lateral_entry
        self.is_alumni = is_alumni
        self.user = user

    def __repr__(self) -> str:
        return f"<Student: {self.f_name} {self.l_name}, {self.dept.short_name}>"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Parent(db.Model):
    __tablename__ = "parent"

    query: BaseQuery

    id = Column(Integer, primary_key=True)

    f_name = Column(Text)
    m_name = Column(Text)
    l_name = Column(Text)
    m_no = Column(Text)

    # Foreign Key
    user_id = Column(Integer, ForeignKey("user.id"))

    # Relationships
    user: User = relationship("User")
    children: List[Student] = relationship(
        "Student", secondary="parent_students", back_populates="parents"
    )

    def __init__(
        self,
        f_name: str,
        l_name: str,
        m_no: str,
        user: User,
        m_name: Optional[str] = None,
    ) -> None:
        self.f_name = f_name
        self.m_name = m_name
        self.l_name = l_name
        self.m_no = m_no
        self.user = user

    def __repr__(self) -> str:
        return f"<Parent: {self.f_name} {self.l_name}>"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


"""USER TABLES"""


class User(db.Model, UserMixin):
    __tablename__ = "user"

    query: BaseQuery

    id = Column(Integer, primary_key=True)

    u_name = Column(Text)
    email = Column(Text)
    password = Column(Text)
    last_active = Column(DateTime(timezone=True))

    # Foreign Key
    role_id = Column(Integer, ForeignKey("role.id"))

    __table_args__ = (UniqueConstraint(u_name, email, role_id),)

    # Relationship
    role: Role = relationship("Role", back_populates="users")

    def __init__(self, u_name: str, email: str, password: str, role: Role) -> None:
        self.u_name = u_name
        self.email = email
        self.password = password
        self.role = role

    def __repr__(self) -> str:
        return f"<User: {self.u_name} - {self.role.role_name}>"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def get_data(self) -> Union[Admin, Staff, Student, Parent]:
        stud = db.session.query(Student).join(User, Student.user_id == self.id).all()
        staff = db.session.query(Staff).join(User, Staff.user_id == self.id).all()
        admin = db.session.query(Admin).join(User, Admin.user_id == self.id).all()
        parent = db.session.query(Parent).join(User, Parent.user_id == self.id).all()
        data = [j for i in (stud, staff, admin, parent) for j in i]
        return data[0]


"""NOTIFICATION TABLES"""


class Notification(db.Model):
    __tablename__ = "notification"

    query: BaseQuery

    id = Column(Integer, primary_key=True)
    content = Column(Text)
    timestamp = Column(DateTime(timezone=True), default=func.now())
    is_read = Column(Boolean, default=False)

    # Foreign Keys
    from_id = Column(Integer, ForeignKey("user.id"))
    to_id = Column(Integer, ForeignKey("user.id"))
    category_id = Column(Integer, ForeignKey("notification_category.id"))

    # Relationships

    from_: User = relationship("User", foreign_keys=from_id)
    to: User = relationship("User", foreign_keys=to_id)
    category: NotificationCategory = relationship(
        "NotificationCategory", back_populates="notifications"
    )

    def __init__(
        self,
        from_: User,
        to: User,
        content: str,
        category: Optional[NotificationCategory] = None,
    ) -> None:
        self.from_ = from_
        self.to = to
        self.content = content
        if category:
            self.category = category

    @classmethod
    def push_notification(
        cls,
        from_: User,
        to: Iterable[User],
        content: str,
        category: Optional[NotificationCategory] = None,
    ) -> Tuple[Notification]:
        notifications: List[Notification] = list()

        for usr in to:
            notifications.append(Notification(from_, usr, content, category))

        return tuple(notifications)
