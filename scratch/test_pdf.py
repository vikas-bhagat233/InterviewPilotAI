import sys
import os

# Add parent directory to path so we can import reports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from reports.pdf_exporter import generate_pdf

def test_pdf_generation():
    print("Initializing PDF generation test...")
    
    # The exact problematic text that caused the crash
    problematic_text = (
        "Here are 15 customized technical interview questions for Vishal Bhagat, "
        "based on his resume, ranging from programming concepts to system design and AI/ML.\n\n"
        "• —\n\n"
        "Interview Questions for Vishal Bhagat\n\n"
        "# 1. SQL - Complex Query & Optimization\n\n"
        "• Question: In your Supply Chain & Inventory Analytics project, you implemented complex SQL queries "
        "for KPIs like inventory turnover and forecast accuracy. Describe a specific scenario where you used SQL "
        "to calculate a non-trivial KPI involving multiple joins and aggregations. How would you optimize this "
        "query if it started performing slowly on a very large dataset?\n"
        "• Core Concepts Tested: Advanced SQL (joins, aggregations, potentially subqueries/CTEs/window functions), "
        "Query Optimization (indexing, EXPLAIN plan, proper join types, efficient filtering).\n"
        "• Model Answer Outline:\n"
        "• Scenario: Detail a KPI calculation (e.g., calculating inventory turnover per product category "
        "over a specific period, requiring joining orders, products, and inventory tables).\n"
        "• Query Description: Explain the tables involved, join conditions, GROUP BY clauses, and aggregation "
        "functions (e.g., SUM(sales) / AVG(inventory)).\n"
        "• Optimization Strategies:\n"
        "• Indexing: Adding indexes to frequently used columns in WHERE, JOIN, and ORDER BY clauses.\n"
        "• EXPLAIN Plan: Using EXPLAIN to understand query execution and identify bottlenecks.\n"
        "• Filtering Early: Applying WHERE clauses as early as possible to reduce the dataset size.\n"
        "• Specific Join Types: Choosing INNER JOIN, LEFT JOIN appropriately.\n"
        "• CTEs/Subqueries: Discussing if CTEs helped readability or if materializing subqueries was considered.\n"
        "* **Avoiding `SELECT *`**: Selecting only necessary columns.\n"
        "• Denormalization (if applicable): Briefly mention if a small amount of redundancy for performance was considered."
    )
    
    results = {
        "resume_analysis": "Mock resume analysis content.",
        "skill_gap": "Mock skill gap content.",
        "hr_questions": "Mock HR questions content.",
        "technical_questions": problematic_text,
        "roadmap": "Mock roadmap content."
    }
    
    output_filename = "test_output_report.pdf"
    
    try:
        generate_pdf(output_filename, results)
        print(f"SUCCESS: PDF successfully generated and saved to {output_filename}!")
        # Clean up
        if os.path.exists(output_filename):
            os.remove(output_filename)
            print("Temporary PDF file cleaned up.")
    except Exception as e:
        print(f"FAILED: PDF generation raised an exception:\n{e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_pdf_generation()
