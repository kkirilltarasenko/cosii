#!/usr/bin/env python3
"""
Главный файл для запуска лабораторных работ по цифровой обработке сигналов.

Лабораторная работа 1: Свертка, корреляция и преобразование Фурье
Лабораторная работа 2: Фильтры (однородный, КИХ, БИХ)

Автор: Тарасенко К.А.
"""

import sys
import os
from pathlib import Path

# Добавляем пути к модулям
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent / "utils"))
sys.path.append(str(Path(__file__).parent / "laba1"))
sys.path.append(str(Path(__file__).parent / "laba2"))

from utils.file_manager import file_manager

def print_header():
    """Выводит заголовок программы"""
    print("=" * 80)
    print("ЛАБОРАТОРНЫЕ РАБОТЫ ПО ЦИФРОВОЙ ОБРАБОТКЕ СИГНАЛОВ")
    print("=" * 80)
    print("Автор: Тарасенко К.А.")
    print("Вариант: БПФ_Ч (БПФ с прореживанием по частоте)")
    print("=" * 80)

def print_menu():
    """Выводит меню выбора"""
    print("\nВыберите действие:")
    print("1. Запустить Лабораторную работу 1 (Свертка, корреляция, БПФ)")
    print("2. Запустить Лабораторную работу 2 (Фильтры)")
    print("3. Запустить обе лабораторные работы")
    print("4. Очистить результаты")
    print("5. Показать структуру файлов")
    print("0. Выход")
    print("-" * 50)

def run_lab1():
    """Запускает лабораторную работу 1"""
    print("\n" + "=" * 60)
    print("ЗАПУСК ЛАБОРАТОРНОЙ РАБОТЫ 1")
    print("=" * 60)
    print("Задачи:")
    print("- Генерация периодических сигналов")
    print("- Реализация свертки и корреляции")
    print("- Прямое и обратное БПФ")
    print("- Построение спектров и временных графиков")
    print("- Сравнение эффективности алгоритмов")
    print("-" * 60)
    
    try:
        # Импортируем и запускаем лабораторную работу 1
        from laba1_runner import run_laba1
        run_laba1()
        print("\n✅ Лабораторная работа 1 выполнена успешно!")
    except Exception as e:
        print(f"\n❌ Ошибка при выполнении лабораторной работы 1: {e}")
        return False
    return True

def run_lab2():
    """Запускает лабораторную работу 2"""
    print("\n" + "=" * 60)
    print("ЗАПУСК ЛАБОРАТОРНОЙ РАБОТЫ 2")
    print("=" * 60)
    print("Задачи:")
    print("- Реализация однородного фильтра")
    print("- Реализация КИХ ВЧ-фильтра с окном Блэкмана")
    print("- Реализация БИХ НЧ-фильтра")
    print("- Анализ эффективности фильтров")
    print("- Построение АЧХ и временных характеристик")
    print("-" * 60)
    
    try:
        # Импортируем и запускаем лабораторную работу 2
        from laba2_runner import run_laba2
        run_laba2()
        print("\n✅ Лабораторная работа 2 выполнена успешно!")
    except Exception as e:
        print(f"\n❌ Ошибка при выполнении лабораторной работы 2: {e}")
        return False
    return True

def clean_results():
    """Очищает все результаты"""
    print("\nОчистка результатов...")
    try:
        file_manager.clean_directory("all")
        print("✅ Все результаты очищены!")
    except Exception as e:
        print(f"❌ Ошибка при очистке: {e}")

def show_file_structure():
    """Показывает структуру созданных файлов"""
    print("\n" + "=" * 60)
    print("СТРУКТУРА ФАЙЛОВ ПРОЕКТА")
    print("=" * 60)
    
    plots = file_manager.list_plots()
    audio = file_manager.list_audio()
    
    print(f"\n📊 Графики ({len(plots)} файлов):")
    if plots:
        for plot in sorted(plots):
            print(f"  - {plot.name}")
    else:
        print("  (нет файлов)")
    
    print(f"\n🔊 Аудиофайлы ({len(audio)} файлов):")
    if audio:
        for audio_file in sorted(audio):
            print(f"  - {audio_file.name}")
    else:
        print("  (нет файлов)")
    
    print(f"\n📁 Структура папок:")
    print("  static/")
    print("  ├── plots/     - графики и диаграммы")
    print("  ├── audio/     - аудиофайлы (.wav)")
    print("  └── data/      - данные и результаты")

def main():
    """Главная функция"""
    print_header()
    
    while True:
        print_menu()
        
        try:
            choice = input("Введите номер действия: ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                run_lab1()
            elif choice == "2":
                run_lab2()
            elif choice == "3":
                print("\n🚀 Запуск обеих лабораторных работ...")
                success1 = run_lab1()
                if success1:
                    success2 = run_lab2()
                    if success1 and success2:
                        print("\n🎉 Обе лабораторные работы выполнены успешно!")
            elif choice == "4":
                clean_results()
            elif choice == "5":
                show_file_structure()
            else:
                print("❌ Неверный выбор. Попробуйте снова.")
                
        except KeyboardInterrupt:
            print("\n\nПрограмма прервана пользователем. До свидания! 👋")
            break
        except Exception as e:
            print(f"\n❌ Произошла ошибка: {e}")
        
        input("\nНажмите Enter для продолжения...")

if __name__ == "__main__":
    main()