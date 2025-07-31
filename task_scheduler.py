#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务调度排期算法实现
基于紧迫度驱动、动态调整、兼顾多样性的设计理念
"""

from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
import json


class ProjectStatus(Enum):
    """项目状态枚举"""
    ACTIVE = "active"
    DELAYED = "delayed"
    COMPLETED = "completed"


class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = "pending"
    OVERDUE = "overdue"
    COMPLETED = "completed"


class Priority(Enum):
    """优先级枚举"""
    HIGH = 1
    MEDIUM = 2
    LOW = 3


@dataclass
class Project:
    """项目数据结构"""
    project_id: str
    name: str
    category: str
    priority: Priority
    deadline: datetime
    status: ProjectStatus = ProjectStatus.ACTIVE

    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            "project_id": self.project_id,
            "name": self.name,
            "category": self.category,
            "priority": self.priority.value,
            "deadline": self.deadline.isoformat(),
            "status": self.status.value
        }


@dataclass
class Task:
    """任务数据结构"""
    task_id: str
    project_id: str
    name: str
    estimated_hours: float
    remaining_hours: float
    status: TaskStatus = TaskStatus.PENDING
    due_date: Optional[datetime] = None

    def __post_init__(self):
        """初始化后处理"""
        if self.remaining_hours is None:
            self.remaining_hours = self.estimated_hours

    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            "task_id": self.task_id,
            "project_id": self.project_id,
            "name": self.name,
            "estimated_hours": self.estimated_hours,
            "remaining_hours": self.remaining_hours,
            "status": self.status.value,
            "due_date": self.due_date.isoformat() if self.due_date else None
        }


@dataclass
class ScheduleEntry:
    """排期条目"""
    task: Task
    allocated_hours: float
    start_time: Optional[str] = None
    end_time: Optional[str] = None

    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            "task_id": self.task.task_id,
            "task_name": self.task.name,
            "allocated_hours": self.allocated_hours,
            "start_time": self.start_time,
            "end_time": self.end_time
        }


class TaskScheduler:
    """任务调度器主类"""

    def __init__(self, daily_work_hours: float = 8.0):
        """
        初始化任务调度器

        Args:
            daily_work_hours: 每日可用工作时间（小时）
        """
        self.projects: Dict[str, Project] = {}
        self.tasks: Dict[str, Task] = {}
        self.schedule: Dict[str, List[ScheduleEntry]] = {}  # 日期 -> 排期条目列表
        self.overdue_queue: List[Task] = []
        self.delayed_projects: List[Project] = []
        self.daily_work_hours = daily_work_hours

        # 紧迫度计算权重系数
        self.w1 = 2.0  # 优先级权重
        self.w2 = 3.0  # 截止日期权重
        self.w3 = 1.5  # 工作量权重

        # 多样性配置
        self.diversity_threshold = 0.1  # 分数差距阈值（10%）
        self.look_ahead_count = 5  # 向前查看的任务数量

    def add_project(self, project: Project) -> None:
        """添加项目"""
        self.projects[project.project_id] = project

    def add_task(self, task: Task) -> None:
        """添加任务"""
        self.tasks[task.task_id] = task

    def get_project_by_id(self, project_id: str) -> Optional[Project]:
        """根据ID获取项目"""
        return self.projects.get(project_id)

    def get_tasks_by_project(self, project_id: str) -> List[Task]:
        """获取项目下的所有任务"""
        return [task for task in self.tasks.values() if task.project_id == project_id]

    def calculate_priority_factor(self, project: Project) -> float:
        """计算优先级因子"""
        priority_map = {
            Priority.HIGH: 1.5,
            Priority.MEDIUM: 1.0,
            Priority.LOW: 0.5
        }
        return priority_map[project.priority]

    def calculate_deadline_factor(self, deadline: datetime, current_date: datetime) -> float:
        """计算截止日期因子"""
        days_until_deadline = (deadline - current_date).days
        return 1.0 / max(1, days_until_deadline)

    def calculate_workload_factor(self, project_id: str, current_date: datetime) -> float:
        """计算工作量因子"""
        project = self.get_project_by_id(project_id)
        if not project:
            return 0.0

        # 计算项目剩余总工时
        project_tasks = self.get_tasks_by_project(project_id)
        total_remaining_hours = sum(
            task.remaining_hours for task in project_tasks
            if task.status == TaskStatus.PENDING
        )

        # 计算到截止日期的天数
        days_until_deadline = max(1, (project.deadline - current_date).days)

        return total_remaining_hours / days_until_deadline

    def calculate_urgency_score(self, task: Task, current_date: datetime) -> float:
        """计算任务的紧迫度分数"""
        project = self.get_project_by_id(task.project_id)
        if not project:
            return 0.0

        # 使用任务的截止日期，如果没有则使用项目截止日期
        deadline = task.due_date if task.due_date else project.deadline

        priority_factor = self.calculate_priority_factor(project)
        deadline_factor = self.calculate_deadline_factor(
            deadline, current_date)
        workload_factor = self.calculate_workload_factor(
            task.project_id, current_date)

        urgency_score = (
            self.w1 * priority_factor +
            self.w2 * deadline_factor +
            self.w3 * workload_factor
        )

        return urgency_score

    def update_overdue_tasks(self, current_date: datetime) -> None:
        """更新逾期任务队列"""
        self.overdue_queue.clear()

        for task in self.tasks.values():
            if task.status != TaskStatus.PENDING:
                continue

            project = self.get_project_by_id(task.project_id)
            if not project or project.status != ProjectStatus.ACTIVE:
                continue

            # 检查任务是否逾期
            deadline = task.due_date if task.due_date else project.deadline
            if deadline < current_date:
                task.status = TaskStatus.OVERDUE
                self.overdue_queue.append(task)

    def get_pending_tasks(self) -> List[Task]:
        """获取所有待处理任务"""
        pending_tasks = []

        for task in self.tasks.values():
            if task.status != TaskStatus.PENDING:
                continue

            project = self.get_project_by_id(task.project_id)
            if project and project.status == ProjectStatus.ACTIVE:
                pending_tasks.append(task)

        return pending_tasks

    def sort_tasks_by_urgency(self, tasks: List[Task], current_date: datetime) -> List[Tuple[Task, float]]:
        """按紧迫度排序任务"""
        task_scores = []

        for task in tasks:
            score = self.calculate_urgency_score(task, current_date)
            task_scores.append((task, score))

        # 按分数降序排序
        task_scores.sort(key=lambda x: x[1], reverse=True)
        return task_scores

    def apply_diversity_rule(self, sorted_tasks: List[Tuple[Task, float]],
                             categories_scheduled_today: set) -> Optional[Tuple[Task, float]]:
        """应用多样性规则选择任务"""
        if not sorted_tasks:
            return None

        # 如果没有安排过任何类别，直接返回最高优先级任务
        if not categories_scheduled_today:
            return sorted_tasks[0]

        # 检查前几个任务，寻找新类别的任务
        highest_score = sorted_tasks[0][1]

        for i, (task, score) in enumerate(sorted_tasks[:self.look_ahead_count]):
            project = self.get_project_by_id(task.project_id)
            if not project:
                continue

            # 如果是新类别，且分数差距在阈值内，优先选择
            if (project.category not in categories_scheduled_today and
                    (highest_score - score) / highest_score <= self.diversity_threshold):
                return (task, score)

        # 如果没有找到合适的新类别任务，返回最高优先级任务
        return sorted_tasks[0]

    def schedule_single_day(self, current_date: datetime,
                            available_hours: float) -> List[ScheduleEntry]:
        """为单天安排任务"""
        daily_schedule = []
        categories_scheduled_today = set()
        remaining_hours = available_hours

        # 首先处理逾期任务
        for task in self.overdue_queue[:]:
            if remaining_hours <= 0:
                break

            project = self.get_project_by_id(task.project_id)
            if not project:
                continue

            # 分配时间
            allocated_hours = min(remaining_hours, task.remaining_hours)
            # 对齐到0.5小时
            allocated_hours = round(allocated_hours * 2) / 2

            if allocated_hours > 0:
                entry = ScheduleEntry(task, allocated_hours)
                daily_schedule.append(entry)

                # 更新任务状态
                task.remaining_hours -= allocated_hours
                if task.remaining_hours <= 0:
                    task.status = TaskStatus.COMPLETED
                    self.overdue_queue.remove(task)

                # 更新状态
                remaining_hours -= allocated_hours
                categories_scheduled_today.add(project.category)

        # 处理常规任务
        pending_tasks = self.get_pending_tasks()
        sorted_tasks = self.sort_tasks_by_urgency(pending_tasks, current_date)

        while remaining_hours > 0 and sorted_tasks:
            # 应用多样性规则选择任务
            selected = self.apply_diversity_rule(
                sorted_tasks, categories_scheduled_today)
            if not selected:
                break

            task, score = selected
            project = self.get_project_by_id(task.project_id)
            if not project:
                sorted_tasks.remove(selected)
                continue

            # 分配时间
            allocated_hours = min(remaining_hours, task.remaining_hours)
            # 对齐到0.5小时
            allocated_hours = round(allocated_hours * 2) / 2

            if allocated_hours > 0:
                entry = ScheduleEntry(task, allocated_hours)
                daily_schedule.append(entry)

                # 更新任务状态
                task.remaining_hours -= allocated_hours
                if task.remaining_hours <= 0:
                    task.status = TaskStatus.COMPLETED

                # 更新状态
                remaining_hours -= allocated_hours
                categories_scheduled_today.add(project.category)

            # 从待选列表中移除已处理的任务
            sorted_tasks.remove(selected)

        return daily_schedule

    def generate_schedule(self, start_date: datetime, max_days: int = 30) -> Dict[str, List[ScheduleEntry]]:
        """生成完整的任务排期"""
        self.schedule.clear()
        current_date = start_date

        for day in range(max_days):
            # 更新逾期任务
            self.update_overdue_tasks(current_date)

            # 检查是否还有待处理任务
            if not self.overdue_queue and not self.get_pending_tasks():
                break

            # 为当天安排任务
            date_str = current_date.strftime('%Y-%m-%d')
            daily_schedule = self.schedule_single_day(
                current_date, self.daily_work_hours)

            if daily_schedule:
                self.schedule[date_str] = daily_schedule

            # 进入下一天
            current_date += timedelta(days=1)

        # 后处理：检查延期项目
        self.check_delayed_projects(current_date)

        return self.schedule

    def check_delayed_projects(self, current_date: datetime) -> None:
        """检查并处理延期项目"""
        self.delayed_projects.clear()

        for project in self.projects.values():
            if project.status != ProjectStatus.ACTIVE:
                continue

            # 检查项目是否有未完成任务且已过截止日期
            if project.deadline < current_date:
                project_tasks = self.get_tasks_by_project(project.project_id)
                has_pending_tasks = any(
                    task.status == TaskStatus.PENDING for task in project_tasks
                )

                if has_pending_tasks:
                    project.status = ProjectStatus.DELAYED
                    self.delayed_projects.append(project)

    def get_schedule_summary(self) -> Dict:
        """获取排期摘要信息"""
        total_days = len(self.schedule)
        total_tasks_scheduled = 0
        total_hours_scheduled = 0.0

        category_hours = {}

        for date, entries in self.schedule.items():
            for entry in entries:
                total_tasks_scheduled += 1
                total_hours_scheduled += entry.allocated_hours

                project = self.get_project_by_id(entry.task.project_id)
                if project:
                    category = project.category
                    category_hours[category] = category_hours.get(
                        category, 0) + entry.allocated_hours

        pending_tasks = len(self.get_pending_tasks())
        overdue_tasks = len(self.overdue_queue)
        delayed_projects = len(self.delayed_projects)

        return {
            "total_days_scheduled": total_days,
            "total_tasks_scheduled": total_tasks_scheduled,
            "total_hours_scheduled": total_hours_scheduled,
            "category_distribution": category_hours,
            "pending_tasks_remaining": pending_tasks,
            "overdue_tasks": overdue_tasks,
            "delayed_projects": delayed_projects
        }

    def export_schedule_to_dict(self) -> Dict:
        """导出排期到字典格式"""
        schedule_dict = {}

        for date, entries in self.schedule.items():
            schedule_dict[date] = [entry.to_dict() for entry in entries]

        return {
            "schedule": schedule_dict,
            "summary": self.get_schedule_summary(),
            "projects": {pid: project.to_dict() for pid, project in self.projects.items()},
            "tasks": {tid: task.to_dict() for tid, task in self.tasks.items()}
        }

    def print_schedule(self) -> None:
        """打印排期结果"""
        print("\n=== 任务排期结果 ===")

        for date in sorted(self.schedule.keys()):
            entries = self.schedule[date]
            print(f"\n📅 {date}:")

            total_hours = 0
            for entry in entries:
                project = self.get_project_by_id(entry.task.project_id)
                category = project.category if project else "未知"
                print(
                    f"  • {entry.task.name} ({category}) - {entry.allocated_hours}小时")
                total_hours += entry.allocated_hours

            print(f"  总计: {total_hours}小时")

        # 打印摘要
        summary = self.get_schedule_summary()
        print(f"\n=== 排期摘要 ===")
        print(f"总排期天数: {summary['total_days_scheduled']}")
        print(f"总任务数: {summary['total_tasks_scheduled']}")
        print(f"总工时: {summary['total_hours_scheduled']}小时")
        print(f"剩余待处理任务: {summary['pending_tasks_remaining']}")
        print(f"逾期任务: {summary['overdue_tasks']}")
        print(f"延期项目: {summary['delayed_projects']}")

        print("\n类别分布:")
        for category, hours in summary['category_distribution'].items():
            print(f"  {category}: {hours}小时")


if __name__ == "__main__":
    # 简单测试
    scheduler = TaskScheduler()

    # 添加测试项目
    project1 = Project(
        project_id="proj1",
        name="网站开发",
        category="研发",
        priority=Priority.HIGH,
        deadline=datetime(2024, 1, 15)
    )
    scheduler.add_project(project1)

    # 添加测试任务
    task1 = Task(
        task_id="task1",
        project_id="proj1",
        name="前端开发",
        estimated_hours=8.0,
        remaining_hours=8.0
    )
    scheduler.add_task(task1)

    # 生成排期
    start_date = datetime(2024, 1, 10)
    schedule = scheduler.generate_schedule(start_date)

    # 打印结果
    scheduler.print_schedule()
