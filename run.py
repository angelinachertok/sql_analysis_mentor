#!/usr/bin/env python3

import sqlite3
import json
import csv
from pathlib import Path
from datetime import datetime

def load_csv_to_database(csv_file, table_name, conn):
    """Load CSV data into SQLite database."""
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            columns = reader.fieldnames
            
            # Create table
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                {', '.join([f"{col} TEXT" for col in columns])}
            )
            """
            conn.execute(create_table_sql)
            
            # Insert data
            for row in reader:
                placeholders = ', '.join(['?' for _ in columns])
                insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
                conn.execute(insert_sql, list(row.values()))
            
            conn.commit()
            return True, f"Loaded {table_name} successfully"
    except Exception as e:
        return False, f"Error loading {table_name}: {str(e)}"

def setup_database():
    """Setup database with CSV data from homework/data/."""
    import os
    conn = sqlite3.connect(':memory:')
    
    data_dir = Path(os.path.join(os.getcwd(), 'homework', 'data'))
    if data_dir.exists():
        for csv_file in data_dir.glob('*.csv'):
            table_name = csv_file.stem
            load_csv_to_database(csv_file, table_name, conn)
    
    return conn

def validate_sql_execution(sql_content, conn):
    """Execute SQL and return results."""
    try:
        cursor = conn.cursor()
        
        # Split SQL content by semicolon and filter empty statements
        sql_statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        if not sql_statements:
            return False, "No valid SQL statements found", None
        
        results = []
        for i, statement in enumerate(sql_statements):
            try:
                cursor.execute(statement)
                
                if statement.strip().upper().startswith('SELECT'):
                    statement_results = cursor.fetchall()
                    results.append(f"Statement {i+1}: {len(statement_results)} rows returned")
                else:
                    conn.commit()
                    results.append(f"Statement {i+1}: Executed successfully")
                    
            except sqlite3.Error as e:
                return False, f"SQL execution failed on statement {i+1}: {str(e)}", None
        
        return True, f"All {len(sql_statements)} statements executed successfully.", results
            
    except sqlite3.Error as e:
        return False, f"SQL execution failed: {str(e)}", None

def check_lesson_files():
    """Check all lesson files."""
    import os
    homework_dir = Path(os.path.join(os.getcwd(), 'homework'))
    test_results = []
    
    # Find student solutions
    lesson_files = []
    for file_path in homework_dir.glob('lesson_*.sql'):
        if not (file_path.name.endswith('_good.sql') or file_path.name.endswith('_perfect.sql')):
            lesson_files.append(file_path)
    
    if not lesson_files:
        test_results.append({
            "name": "sql_lessons",
            "status": "skipped",
            "message": "No SQL lesson files found (excluding _good and _perfect)",
            "details": {}
        })
        return test_results
    
    # Setup database
    conn = setup_database()
    
    for lesson_file in lesson_files:
        lesson_name = lesson_file.stem
        
        try:
            with open(lesson_file, 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            success, message, details = validate_sql_execution(sql_content, conn)
            
            test_results.append({
                "name": lesson_name,
                "status": "passed" if success else "failed",
                "message": message,
                "details": details or {}
            })
            
        except Exception as e:
            test_results.append({
                "name": lesson_name,
                "status": "error",
                "message": f"Error processing {lesson_name}: {str(e)}",
                "details": {}
            })
    
    conn.close()
    return test_results

def main():
    """Main function to run all tests."""
    import os
    test_results_dir = Path(os.environ.get('RESULTS_DIR', '/mnt/results'))
    test_results_dir.mkdir(exist_ok=True)
    
    test_results = []
    
    # Check SQL lesson files
    sql_results = check_lesson_files()
    test_results.extend(sql_results)
    
    # Save results as JUnit XML
    total_tests = len(test_results)
    passed_tests = len([r for r in test_results if r["status"] == "passed"])
    failed_tests = len([r for r in test_results if r["status"] == "failed"])
    error_tests = len([r for r in test_results if r["status"] == "error"])
    skipped_tests = len([r for r in test_results if r["status"] == "skipped"])
    
    xml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<testsuites name="SQL Analysis Tests" tests="{total_tests}" failures="{failed_tests}" errors="{error_tests}" skipped="{skipped_tests}">
    <testsuite name="SQL Lessons" tests="{total_tests}" failures="{failed_tests}" errors="{error_tests}" skipped="{skipped_tests}">
'''
    
    for result in test_results:
        status = "passed" if result["status"] == "passed" else "failed" if result["status"] == "failed" else "error" if result["status"] == "error" else "skipped"
        xml_content += f'''        <testcase name="{result['name']}" classname="SQLTests" status="{status}">
'''
        if status in ["failed", "error"]:
            xml_content += f'''            <failure message="{result['message']}">{result.get('details', '')}</failure>
'''
        elif status == "skipped":
            xml_content += f'''            <skipped message="{result['message']}"/>
'''
        xml_content += '''        </testcase>
'''
    
    xml_content += '''    </testsuite>
</testsuites>'''
    
    with open(test_results_dir / 'results.xml', 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"Test completed: {passed_tests}/{total_tests} passed")
    return results_data

if __name__ == "__main__":
    main()
