#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务调度算法测试脚本
用于测试各种场景下的任务调度效果
"""

import json
from datetime import datetime
from task_scheduler import TaskScheduler, Project, Task, Priority, ProjectStatus, TaskStatus


class SchedulerTester:
    """任务调度器测试类"""
    
    def __init__(self, test_data_file: str = "test_data.json"):
        """
        初始化测试器
        
        Args:
            test_data_file: 测试数据文件路径
        """
        self.test_data_file = test_data_file
        self.test_data = None
        self.load_test_data()
    
    def load_test_data(self) -> None:
        """加载测试数据"""
        try:
            with open(self.test_data_file, 'r', encoding='utf-8') as f:
                self.test_data = json.load(f)
            print(f"✅ 成功加载测试数据: {self.test_data_file}")
        except FileNotFoundError:
            print(f"❌ 测试数据文件未找到: {self.test_data_file}")
            raise
        except json.JSONDecodeError as e:
            print(f"❌ 测试数据JSON格式错误: {e}")
            raise
    
    def create_scheduler_from_data(self) -> TaskScheduler:
        """根据测试数据创建调度器实例"""
        config = self.test_data.get('scheduler_config', {})
        daily_hours = config.get('daily_work_hours', 8.0)
        
        scheduler = TaskScheduler(daily_work_hours=daily_hours)
        
        # 设置权重参数
        weights = config.get('weights', {})
        scheduler.w1 = weights.get('priority_weight', 2.0)
        scheduler.w2 = weights.get('deadline_weight', 3.0)
        scheduler.w3 = weights.get('workload_weight', 1.5)
        
        # 设置多样性参数
        diversity = config.get('diversity_config', {})
        scheduler.diversity_threshold = diversity.get('diversity_threshold', 0.1)
        scheduler.look_ahead_count = diversity.get('look_ahead_count', 5)
        
        return scheduler
    
    def load_projects_and_tasks(self, scheduler: TaskScheduler) -> None:
        """加载项目和任务数据到调度器"""
        # 加载项目
        for proj_data in self.test_data['projects']:
            project = Project(
                project_id=proj_data['project_id'],
                name=proj_data['name'],
                category=proj_data['category'],
                priority=Priority(proj_data['priority']),
                deadline=datetime.fromisoformat(proj_data['deadline']),
                status=ProjectStatus(proj_data['status'])
            )
            scheduler.add_project(project)
        
        # 加载任务
        for task_data in self.test_data['tasks']:
            task = Task(
                task_id=task_data['task_id'],
                project_id=task_data['project_id'],
                name=task_data['name'],
                estimated_hours=task_data['estimated_hours'],
                remaining_hours=task_data['remaining_hours'],
                status=TaskStatus(task_data['status']),
                due_date=datetime.fromisoformat(task_data['due_date']) if task_data.get('due_date') else None
            )
            scheduler.add_task(task)
        
        print(f"✅ 加载了 {len(scheduler.projects)} 个项目和 {len(scheduler.tasks)} 个任务")
    
    def run_basic_test(self) -> None:
        """运行基础功能测试"""
        print("\n" + "="*50)
        print("🧪 基础功能测试")
        print("="*50)
        
        scheduler = self.create_scheduler_from_data()
        self.load_projects_and_tasks(scheduler)
        
        # 使用配置中的开始日期
        start_date = datetime.fromisoformat(self.test_data['scheduler_config']['start_date'])
        
        print(f"\n📅 开始日期: {start_date.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"⏰ 每日工作时间: {scheduler.daily_work_hours} 小时")
        
        # 生成排期
        schedule = scheduler.generate_schedule(start_date, max_days=20)
        
        # 打印排期结果
        scheduler.print_schedule()
        
        # 验证基本约束
        self.validate_basic_constraints(scheduler)
        
        return scheduler
    
    def validate_basic_constraints(self, scheduler: TaskScheduler) -> None:
        """验证基本约束条件"""
        print("\n🔍 验证基本约束条件...")
        
        violations = []
        
        # 检查每日工时不超限
        for date, entries in scheduler.schedule.items():
            daily_hours = sum(entry.allocated_hours for entry in entries)
            if daily_hours > scheduler.daily_work_hours + 0.1:  # 允许0.1小时误差
                violations.append(f"日期 {date} 工时超限: {daily_hours} > {scheduler.daily_work_hours}")
        
        # 检查任务时间分配的合理性
        for task in scheduler.tasks.values():
            if task.remaining_hours < 0:
                violations.append(f"任务 {task.name} 剩余工时为负: {task.remaining_hours}")
        
        # 检查时间分配是否为0.5的倍数
        for date, entries in scheduler.schedule.items():
            for entry in entries:
                if entry.allocated_hours % 0.5 != 0:
                    violations.append(f"任务 {entry.task.name} 在 {date} 的分配时间不是0.5的倍数: {entry.allocated_hours}")
        
        if violations:
            print("❌ 发现约束违反:")
            for violation in violations:
                print(f"  • {violation}")
        else:
            print("✅ 所有基本约束条件满足")
    
    def test_overdue_handling(self) -> None:
        """测试逾期任务处理"""
        print("\n" + "="*50)
        print("🧪 逾期任务处理测试")
        print("="*50)
        
        scheduler = self.create_scheduler_from_data()
        self.load_projects_and_tasks(scheduler)
        
        # 使用较晚的开始日期，使某些任务逾期
        start_date = datetime(2024, 1, 17, 9, 0, 0)
        print(f"\n📅 开始日期: {start_date.strftime('%Y-%m-%d %H:%M:%S')} (故意设置较晚)")
        
        # 更新逾期任务
        scheduler.update_overdue_tasks(start_date)
        
        print(f"\n⚠️ 检测到 {len(scheduler.overdue_queue)} 个逾期任务:")
        for task in scheduler.overdue_queue:
            project = scheduler.get_project_by_id(task.project_id)
            due_date = task.due_date if task.due_date else project.deadline
            print(f"  • {task.name} (截止: {due_date.strftime('%Y-%m-%d')})")
        
        # 生成排期
        schedule = scheduler.generate_schedule(start_date, max_days=15)
        
        # 验证逾期任务是否优先安排
        self.validate_overdue_priority(scheduler)
        
        # 打印前几天的排期
        print("\n📋 前3天排期 (验证逾期任务优先级):")
        dates = sorted(scheduler.schedule.keys())[:3]
        for date in dates:
            entries = scheduler.schedule[date]
            print(f"\n📅 {date}:")
            for entry in entries:
                status_mark = "⚠️" if entry.task.status == TaskStatus.OVERDUE else "📝"
                print(f"  {status_mark} {entry.task.name} - {entry.allocated_hours}小时")
    
    def validate_overdue_priority(self, scheduler: TaskScheduler) -> None:
        """验证逾期任务优先级"""
        print("\n🔍 验证逾期任务优先级...")
        
        if not scheduler.overdue_queue:
            print("✅ 无逾期任务需要验证")
            return
        
        # 检查前几天的排期中是否优先安排了逾期任务
        first_few_days = sorted(scheduler.schedule.keys())[:3]
        overdue_scheduled_early = False
        
        for date in first_few_days:
            entries = scheduler.schedule.get(date, [])
            for entry in entries:
                if entry.task in scheduler.overdue_queue:
                    overdue_scheduled_early = True
                    break
            if overdue_scheduled_early:
                break
        
        if overdue_scheduled_early:
            print("✅ 逾期任务在前几天得到优先安排")
        else:
            print("❌ 逾期任务未能优先安排")
    
    def test_diversity_rule(self) -> None:
        """测试多样性规则"""
        print("\n" + "="*50)
        print("🧪 多样性规则测试")
        print("="*50)
        
        scheduler = self.create_scheduler_from_data()
        self.load_projects_and_tasks(scheduler)
        
        start_date = datetime(2024, 1, 15, 9, 0, 0)
        
        # 生成排期
        schedule = scheduler.generate_schedule(start_date, max_days=10)
        
        # 分析每日类别分布
        self.analyze_daily_diversity(scheduler)
    
    def analyze_daily_diversity(self, scheduler: TaskScheduler) -> None:
        """分析每日工作类别多样性"""
        print("\n📊 每日工作类别分布分析:")
        
        for date in sorted(scheduler.schedule.keys()):
            entries = scheduler.schedule[date]
            categories = {}
            
            for entry in entries:
                project = scheduler.get_project_by_id(entry.task.project_id)
                if project:
                    category = project.category
                    categories[category] = categories.get(category, 0) + entry.allocated_hours
            
            print(f"\n📅 {date}:")
            for category, hours in categories.items():
                print(f"  • {category}: {hours}小时")
            
            # 检查是否有良好的多样性
            if len(categories) > 1:
                print("  ✅ 类别多样性良好")
            elif len(categories) == 1:
                print("  ⚠️ 只有一个工作类别")
    
    def test_urgency_calculation(self) -> None:
        """测试紧迫度计算"""
        print("\n" + "="*50)
        print("🧪 紧迫度计算测试")
        print("="*50)
        
        scheduler = self.create_scheduler_from_data()
        self.load_projects_and_tasks(scheduler)
        
        start_date = datetime(2024, 1, 15, 9, 0, 0)
        
        print("\n📊 任务紧迫度分析:")
        
        # 获取所有待处理任务
        pending_tasks = scheduler.get_pending_tasks()
        
        # 计算并显示紧迫度分数
        task_scores = []
        for task in pending_tasks:
            score = scheduler.calculate_urgency_score(task, start_date)
            task_scores.append((task, score))
        
        # 按分数排序
        task_scores.sort(key=lambda x: x[1], reverse=True)
        
        print(f"\n排序后的任务列表 (共{len(task_scores)}个):")
        for i, (task, score) in enumerate(task_scores[:10]):  # 只显示前10个
            project = scheduler.get_project_by_id(task.project_id)
            due_date = task.due_date if task.due_date else project.deadline
            days_left = (due_date - start_date).days
            
            print(f"{i+1:2d}. {task.name:<25} | 分数: {score:6.2f} | 剩余天数: {days_left:2d} | 类别: {project.category}")
    
    def export_test_results(self, scheduler: TaskScheduler, filename: str = "test_results.json") -> None:
        """导出测试结果"""
        print(f"\n💾 导出测试结果到 {filename}...")
        
        results = scheduler.export_schedule_to_dict()
        
        # 添加测试元数据
        results['test_metadata'] = {
            'test_date': datetime.now().isoformat(),
            'test_data_file': self.test_data_file,
            'scheduler_config': self.test_data.get('scheduler_config', {})
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"✅ 测试结果已导出到 {filename}")
        except Exception as e:
            print(f"❌ 导出失败: {e}")
    
    def run_all_tests(self) -> None:
        """运行所有测试"""
        print("🚀 开始运行任务调度算法测试套件")
        print("="*60)
        
        try:
            # 基础功能测试
            scheduler = self.run_basic_test()
            
            # 逾期任务处理测试
            self.test_overdue_handling()
            
            # 多样性规则测试
            self.test_diversity_rule()
            
            # 紧迫度计算测试
            self.test_urgency_calculation()
            
            # 导出测试结果
            self.export_test_results(scheduler)
            
            print("\n" + "="*60)
            print("🎉 所有测试完成!")
            
        except Exception as e:
            print(f"\n❌ 测试过程中发生错误: {e}")
            raise


def main():
    """主函数"""
    try:
        tester = SchedulerTester()
        tester.run_all_tests()
    except Exception as e:
        print(f"程序执行失败: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())