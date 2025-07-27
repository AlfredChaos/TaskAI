#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
任务调度算法演示脚本
提供交互式界面展示算法功能
"""

import json
from datetime import datetime, timedelta
from task_scheduler import TaskScheduler, Project, Task, Priority, ProjectStatus, TaskStatus


class SchedulerDemo:
    """任务调度器演示类"""
    
    def __init__(self):
        self.scheduler = TaskScheduler()
        self.setup_demo_data()
    
    def setup_demo_data(self) -> None:
        """设置演示数据"""
        print("🔧 正在设置演示数据...")
        
        # 创建演示项目
        projects = [
            Project(
                project_id="demo_web",
                name="公司官网重构",
                category="研发",
                priority=Priority.HIGH,
                deadline=datetime(2024, 2, 1)
            ),
            Project(
                project_id="demo_marketing",
                name="春节营销活动",
                category="市场营销",
                priority=Priority.HIGH,
                deadline=datetime(2024, 1, 25)
            ),
            Project(
                project_id="demo_training",
                name="团队技能培训",
                category="学习",
                priority=Priority.MEDIUM,
                deadline=datetime(2024, 2, 15)
            ),
            Project(
                project_id="demo_personal",
                name="个人发展计划",
                category="生活",
                priority=Priority.LOW,
                deadline=datetime(2024, 3, 1)
            )
        ]
        
        # 创建演示任务
        tasks = [
            # 网站重构项目任务
            Task("task_web_1", "demo_web", "需求分析和设计", 6.0, 6.0, due_date=datetime(2024, 1, 20)),
            Task("task_web_2", "demo_web", "前端开发", 16.0, 16.0, due_date=datetime(2024, 1, 28)),
            Task("task_web_3", "demo_web", "后端开发", 12.0, 12.0, due_date=datetime(2024, 1, 30)),
            Task("task_web_4", "demo_web", "测试和部署", 4.0, 4.0, due_date=datetime(2024, 2, 1)),
            
            # 营销活动任务
            Task("task_mkt_1", "demo_marketing", "活动策划", 4.0, 4.0, due_date=datetime(2024, 1, 18)),
            Task("task_mkt_2", "demo_marketing", "素材制作", 6.0, 6.0, due_date=datetime(2024, 1, 22)),
            Task("task_mkt_3", "demo_marketing", "渠道投放", 2.0, 2.0, due_date=datetime(2024, 1, 24)),
            Task("task_mkt_4", "demo_marketing", "效果监控", 2.0, 2.0, due_date=datetime(2024, 1, 25)),
            
            # 培训项目任务
            Task("task_train_1", "demo_training", "培训需求调研", 2.0, 2.0, due_date=datetime(2024, 1, 25)),
            Task("task_train_2", "demo_training", "课程设计", 8.0, 8.0, due_date=datetime(2024, 2, 5)),
            Task("task_train_3", "demo_training", "培训实施", 12.0, 12.0, due_date=datetime(2024, 2, 12)),
            
            # 个人发展任务
            Task("task_personal_1", "demo_personal", "制定学习计划", 1.0, 1.0, due_date=datetime(2024, 1, 30)),
            Task("task_personal_2", "demo_personal", "技能学习", 20.0, 20.0, due_date=datetime(2024, 2, 28)),
            Task("task_personal_3", "demo_personal", "总结反思", 2.0, 2.0, due_date=datetime(2024, 3, 1))
        ]
        
        # 添加到调度器
        for project in projects:
            self.scheduler.add_project(project)
        
        for task in tasks:
            self.scheduler.add_task(task)
        
        print(f"✅ 演示数据设置完成: {len(projects)}个项目, {len(tasks)}个任务")
    
    def show_projects_overview(self) -> None:
        """显示项目概览"""
        print("\n" + "="*60)
        print("📋 项目概览")
        print("="*60)
        
        for project in self.scheduler.projects.values():
            tasks = self.scheduler.get_tasks_by_project(project.project_id)
            total_hours = sum(task.estimated_hours for task in tasks)
            remaining_hours = sum(task.remaining_hours for task in tasks if task.status == TaskStatus.PENDING)
            
            priority_str = {Priority.HIGH: "高", Priority.MEDIUM: "中", Priority.LOW: "低"}[project.priority]
            
            print(f"\n📁 {project.name}")
            print(f"   类别: {project.category} | 优先级: {priority_str} | 截止: {project.deadline.strftime('%Y-%m-%d')}")
            print(f"   总工时: {total_hours}h | 剩余: {remaining_hours}h | 任务数: {len(tasks)}")
            
            # 显示任务列表
            for task in tasks:
                status_icon = {TaskStatus.PENDING: "⏳", TaskStatus.COMPLETED: "✅", TaskStatus.OVERDUE: "⚠️"}[task.status]
                print(f"     {status_icon} {task.name} ({task.remaining_hours}h)")
    
    def interactive_schedule(self) -> None:
        """交互式排期"""
        print("\n" + "="*60)
        print("🎯 交互式任务排期")
        print("="*60)
        
        # 获取用户输入的开始日期
        while True:
            try:
                date_input = input("\n请输入排期开始日期 (格式: YYYY-MM-DD, 回车使用今天): ").strip()
                if not date_input:
                    start_date = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
                else:
                    start_date = datetime.strptime(date_input, "%Y-%m-%d").replace(hour=9, minute=0, second=0, microsecond=0)
                break
            except ValueError:
                print("❌ 日期格式错误，请使用 YYYY-MM-DD 格式")
        
        # 获取每日工作时间
        while True:
            try:
                hours_input = input(f"请输入每日工作时间 (小时, 回车使用默认{self.scheduler.daily_work_hours}h): ").strip()
                if not hours_input:
                    break
                daily_hours = float(hours_input)
                if daily_hours > 0:
                    self.scheduler.daily_work_hours = daily_hours
                    break
                else:
                    print("❌ 工作时间必须大于0")
            except ValueError:
                print("❌ 请输入有效的数字")
        
        print(f"\n🚀 开始生成排期...")
        print(f"📅 开始日期: {start_date.strftime('%Y-%m-%d %H:%M')}")
        print(f"⏰ 每日工作时间: {self.scheduler.daily_work_hours}小时")
        
        # 生成排期
        schedule = self.scheduler.generate_schedule(start_date, max_days=30)
        
        if not schedule:
            print("\n❌ 没有生成任何排期，可能所有任务都已完成")
            return
        
        # 显示排期结果
        self.scheduler.print_schedule()
        
        # 询问是否导出结果
        export = input("\n是否导出排期结果到JSON文件? (y/N): ").strip().lower()
        if export in ['y', 'yes']:
            filename = f"schedule_{start_date.strftime('%Y%m%d')}.json"
            self.export_schedule(filename)
    
    def export_schedule(self, filename: str) -> None:
        """导出排期结果"""
        try:
            results = self.scheduler.export_schedule_to_dict()
            
            # 添加导出元数据
            results['export_metadata'] = {
                'export_time': datetime.now().isoformat(),
                'scheduler_version': '1.0',
                'daily_work_hours': self.scheduler.daily_work_hours
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 排期结果已导出到 {filename}")
        except Exception as e:
            print(f"❌ 导出失败: {e}")
    
    def simulate_work_progress(self) -> None:
        """模拟工作进度"""
        print("\n" + "="*60)
        print("⚡ 工作进度模拟")
        print("="*60)
        
        # 随机完成一些任务
        import random
        
        pending_tasks = [task for task in self.scheduler.tasks.values() if task.status == TaskStatus.PENDING]
        
        if not pending_tasks:
            print("没有待处理的任务可以模拟")
            return
        
        # 随机选择几个任务进行进度模拟
        num_to_simulate = min(3, len(pending_tasks))
        tasks_to_simulate = random.sample(pending_tasks, num_to_simulate)
        
        print("\n🎲 随机模拟以下任务的进度:")
        
        for task in tasks_to_simulate:
            # 随机完成一部分工作
            progress_ratio = random.uniform(0.2, 0.8)
            completed_hours = task.estimated_hours * progress_ratio
            task.remaining_hours = max(0, task.estimated_hours - completed_hours)
            
            if task.remaining_hours == 0:
                task.status = TaskStatus.COMPLETED
                status_text = "✅ 已完成"
            else:
                status_text = f"⏳ 剩余 {task.remaining_hours:.1f}h"
            
            print(f"  • {task.name}: 完成 {completed_hours:.1f}h / {task.estimated_hours}h ({status_text})")
        
        print("\n💡 提示: 现在可以重新生成排期，看看进度更新后的效果")
    
    def show_urgency_analysis(self) -> None:
        """显示紧迫度分析"""
        print("\n" + "="*60)
        print("📊 任务紧迫度分析")
        print("="*60)
        
        current_date = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        pending_tasks = self.scheduler.get_pending_tasks()
        
        if not pending_tasks:
            print("没有待处理的任务")
            return
        
        # 计算紧迫度分数
        task_scores = []
        for task in pending_tasks:
            score = self.scheduler.calculate_urgency_score(task, current_date)
            task_scores.append((task, score))
        
        # 排序
        task_scores.sort(key=lambda x: x[1], reverse=True)
        
        print(f"\n基于当前时间 {current_date.strftime('%Y-%m-%d')} 的紧迫度排序:")
        print("\n排名 | 任务名称                | 紧迫度 | 剩余天数 | 项目类别")
        print("-" * 70)
        
        for i, (task, score) in enumerate(task_scores, 1):
            project = self.scheduler.get_project_by_id(task.project_id)
            due_date = task.due_date if task.due_date else project.deadline
            days_left = (due_date - current_date).days
            
            print(f"{i:3d}  | {task.name:<23} | {score:6.2f} | {days_left:6d}   | {project.category}")
    
    def show_menu(self) -> None:
        """显示主菜单"""
        print("\n" + "="*60)
        print("🎮 任务调度算法演示系统")
        print("="*60)
        print("1. 查看项目概览")
        print("2. 交互式任务排期")
        print("3. 紧迫度分析")
        print("4. 模拟工作进度")
        print("5. 重置演示数据")
        print("0. 退出")
        print("-" * 60)
    
    def reset_demo_data(self) -> None:
        """重置演示数据"""
        print("\n🔄 重置演示数据...")
        self.scheduler = TaskScheduler()
        self.setup_demo_data()
        print("✅ 演示数据已重置")
    
    def run(self) -> None:
        """运行演示"""
        print("🌟 欢迎使用任务调度算法演示系统!")
        print("\n本系统展示了基于'紧迫度驱动、动态调整、兼顾多样性'理念的任务调度算法")
        
        while True:
            self.show_menu()
            
            try:
                choice = input("请选择操作 (0-5): ").strip()
                
                if choice == '0':
                    print("\n👋 感谢使用任务调度算法演示系统!")
                    break
                elif choice == '1':
                    self.show_projects_overview()
                elif choice == '2':
                    self.interactive_schedule()
                elif choice == '3':
                    self.show_urgency_analysis()
                elif choice == '4':
                    self.simulate_work_progress()
                elif choice == '5':
                    self.reset_demo_data()
                else:
                    print("❌ 无效选择，请输入 0-5 之间的数字")
                
                input("\n按回车键继续...")
                
            except KeyboardInterrupt:
                print("\n\n👋 程序被用户中断，再见!")
                break
            except Exception as e:
                print(f"\n❌ 发生错误: {e}")
                input("按回车键继续...")


def main():
    """主函数"""
    try:
        demo = SchedulerDemo()
        demo.run()
    except Exception as e:
        print(f"程序启动失败: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())