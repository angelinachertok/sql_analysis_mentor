# BDL Module 02 - SQL Analysis (Mentor Repository)

## Структура репозитория

```
bdl-module-02-sql-analysis-mentor/
├── homework/
│   ├── data/
│   │   ├── products.csv
│   │   └── sales.csv
│   ├── lesson_1_good.sql
│   ├── lesson_1_perfect.sql
│   ├── lesson_2_good.sql
│   ├── lesson_2_perfect.sql
│   └── run.py
└── README.md
```

## Назначение

Этот репозиторий содержит:
- Базу данных с тестовыми данными (CSV файлы)
- Эталонные решения для проверки (good/perfect)
- Тестовый раннер `run.py` для автоматической проверки

## Как работает

1. Студенты форкают этот репозиторий
2. Добавляют свои решения в файлы `lesson_X.sql`
3. SandboxApi запускает `run.py` для проверки решений
4. Результаты сохраняются в `results.json`

## Тестирование

Запуск тестов:
```bash
python homework/run.py
```

Результаты будут в `homework/TestResults/results.json`

