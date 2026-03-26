#!/usr/bin/env python3
"""
MelaniaBot: AI Homeschooling Assistant
Simulates an educational robot tutor for homeschooling
"""

import json
import time
import random
from datetime import datetime
from typing import Dict, List, Tuple

class MelaniaBot:
    def __init__(self, student_name: str):
        self.student_name = student_name
        self.lessons_completed = 0
        self.score_history = []
        self.current_subject = None
        self.session_start = None
        self.knowledge_base = {
            'math': [
                {'question': 'What is 7 × 8?', 'answer': '56', 'explanation': 'Seven groups of eight equals fifty-six.'},
                {'question': 'Solve: 3x + 5 = 20', 'answer': '5', 'explanation': 'Subtract 5 from both sides: 3x=15, then divide by 3: x=5.'},
                {'question': 'What is the area of a circle with radius 3?', 'answer': '28.27', 'explanation': 'Area = πr² ≈ 3.14159 × 9 ≈ 28.27'},
            ],
            'history': [
                {'question': 'In what year did the American Revolution begin?', 'answer': '1775', 'explanation': 'The Battles of Lexington and Concord started in April 1775.'},
                {'question': 'Who wrote the Declaration of Independence?', 'answer': 'Thomas Jefferson', 'explanation': 'Jefferson was the primary author, drafted in June 1776.'},
                {'question': 'What was the Louisiana Purchase?', 'answer': '1803 land acquisition from France', 'explanation': 'The US bought 828,000 square miles from Napoleon for $15 million.'},
            ],
            'science': [
                {'question': 'What is the chemical symbol for water?', 'answer': 'H2O', 'explanation': 'Two hydrogen atoms bonded to one oxygen atom.'},
                {'question': 'What causes the seasons on Earth?', 'answer': 'Axial tilt', 'explanation': 'Earth\'s 23.5° tilt causes varying sunlight intensity throughout the year.'},
                {'question': 'What is the powerhouse of the cell?', 'answer': 'Mitochondria', 'explanation': 'Mitochondria produce ATP through cellular respiration.'},
            ]
        }
    
    def greet(self) -> str:
        return f"Hello, {self.student_name}! I'm MelaniaBot, your AI homeschooling assistant. 🇺🇸\nLet's make learning great again!"
    
    def start_session(self):
        self.session_start = datetime.now()
        print(f"\n📚 Session started at {self.session_start.strftime('%H:%M')}")
        print("Available subjects: Math, History, Science, Personalized Plan")
    
    def list_subjects(self) -> List[str]:
        return list(self.knowledge_base.keys())
    
    def get_lesson(self, subject: str) -> Dict:
        """Retrieve a random lesson from the knowledge base"""
        if subject.lower() not in self.knowledge_base:
            return {'error': 'Subject not available'}
        
        lesson = random.choice(self.knowledge_base[subject.lower()])
        self.current_subject = subject.lower()
        return {
            'subject': subject,
            'question': lesson['question'],
            'hint': "Think carefully! I'll give you the explanation after you answer." if random.random() > 0.5 else None
        }
    
    def evaluate_answer(self, user_answer: str, correct_answer: str, explanation: str) -> Dict:
        """Check student's answer and provide feedback"""
        cleaned_user = user_answer.strip().lower()
        cleaned_correct = correct_answer.strip().lower()
        
        # Simple string matching (could be enhanced with NLP)
        is_correct = cleaned_user == cleaned_correct or cleaned_correct in cleaned_user
        
        if is_correct:
            score = 1.0
            feedback = "✅ Excellent! You're a top student!"
            self.score_history.append(score)
        else:
            score = 0.0
            feedback = f"❌ Not quite. The correct answer is: {correct_answer}\n💡 {explanation}"
        
        self.lessons_completed += 1
        return {
            'correct': is_correct,
            'score': score,
            'feedback': feedback,
            'lessons_completed': self.lessons_completed
        }
    
    def get_progress_report(self) -> str:
        """Generate a simple progress report"""
        total = len(self.score_history)
        if total == 0:
            return "No lessons completed yet. Start learning!"
        
        correct = sum(self.score_history)
        accuracy = (correct / total) * 100
        
        grade = 'A+' if accuracy >= 95 else 'A' if accuracy >= 90 else 'B+' if accuracy >= 85 else 'B' if accuracy >= 80 else 'C'
        
        report = f"""
╔══════════════════════════════════════╗
║     🎓 Homeschool Progress Report     ║
╠══════════════════════════════════════╣
║ Student: {self.student_name:<24} ║
║ Lessons Completed: {total:<19} ║
║ Accuracy: {accuracy:.1f}%{'':<15} ║
║ Current Grade: {grade:<19} ║
╚══════════════════════════════════════╝
"""
        return report
    
    def motivational_quote(self) -> str:
        quotes = [
            "Education is the most powerful weapon which you can use to change the world. - Nelson Mandela",
            "The beautiful thing about learning is no one can take it away from you. - B.B. King",
            "In a world where you can be anything, be kind. And also be smart!",
            "Your potential is endless. Your education is the key.",
            "Every child is an artist. The problem is staying an artist when you grow up. - Picasso"
        ]
        return random.choice(quotes)
    
    def end_session(self):
        if self.session_start:
            duration = datetime.now() - self.session_start
            print(f"\n🏁 Session ended. Duration: {duration.seconds // 60} minutes")
            print(self.get_progress_report())
            print(f"\n💭 {self.motivational_quote()}")
            print("\nGod Bless America! 🇺🇸\n")

def interactive_mode():
    """Run the bot in interactive command-line mode"""
    print("=" * 50)
    print("🎓 MELANIABOT - AI Homeschooling Assistant")
    print("=" * 50)
    
    student = input("Enter student name: ").strip() or "Student"
    bot = MelaniaBot(student)
    print(bot.greet())
    
    bot.start_session()
    
    while True:
        print("\n" + "-" * 30)
        print("Commands: subjects, lesson, answer, progress, quote, exit")
        cmd = input("→ ").strip().lower()
        
        if cmd == 'exit':
            bot.end_session()
            break
        
        elif cmd == 'subjects':
            subjects = bot.list_subjects()
            print(f"\n📚 Available subjects: {', '.join(subjects)}")
        
        elif cmd == 'lesson':
            subject = input("Select subject (math/history/science): ").strip()
            lesson = bot.get_lesson(subject)
            if 'error' in lesson:
                print(f"⚠️  {lesson['error']}")
            else:
                print(f"\n📖 {lesson['subject'].upper()} LESSON")
                print(f"Question: {lesson['question']}")
                if lesson['hint']:
                    print(f"💡 Hint: {lesson['hint']}")
        
        elif cmd == 'answer':
            if bot.current_subject:
                user_answer = input("Your answer: ").strip()
                # Get the last lesson from knowledge base (in real app, would track current question)
                lessons = bot.knowledge_base[bot.current_subject]
                current_lesson = random.choice(lessons)  # Simplified
                result = bot.evaluate_answer(user_answer, current_lesson['answer'], current_lesson['explanation'])
                print(f"\n{result['feedback']}")
                print(f"📊 Total lessons: {result['lessons_completed']}")
            else:
                print("⚠️  Start a lesson first with 'lesson' command")
        
        elif cmd == 'progress':
            print(bot.get_progress_report())
        
        elif cmd == 'quote':
            print(f"\n✨ {bot.motivational_quote()}")
        
        else:
            print("❌ Unknown command. Try: subjects, lesson, answer, progress, quote, exit")

def simulation_mode():
    """Run a simulation with sample interactions"""
    print("\n🤖 Running simulation with sample student 'Barron'...\n")
    
    bot = MelaniaBot("Barron")
    print(bot.greet())
    bot.start_session()
    
    # Simulate 5 lessons across different subjects
    subjects = ['math', 'history', 'science']
    
    for i in range(5):
        subject = subjects[i % 3]
        lesson = bot.get_lesson(subject)
        print(f"\n📖 Lesson {i+1}: {lesson['subject'].upper()}")
        print(f"Q: {lesson['question']}")
        
        # Simulate student answers (80% correct)
        if random.random() < 0.8:
            answer = lesson['explanation'].split('.')[0]  # Simulate partial knowledge
            result = bot.evaluate_answer(lesson['answer'][:10], lesson['answer'], lesson['explanation'])
        else:
            result = bot.evaluate_answer("wrong answer", lesson['answer'], lesson['explanation'])
        
        print(result['feedback'])
        time.sleep(1)
    
    bot.end_session()

def main():
    """Entry point with mode selection"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--sim':
        simulation_mode()
    else:
        try:
            interactive_mode()
        except KeyboardInterrupt:
            print("\n\n👋 Session interrupted. Goodbye!")
            sys.exit(0)

if __name__ == "__main__":
    main()