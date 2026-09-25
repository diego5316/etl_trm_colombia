from src.extract import fetch_all, save_raw
from src.transform import load_raw, clean, save_processed
from src.load import load_clean_csv, load_to_sqlite
from src.visualize import load_data, plot_evolution, plot_monthly_average


def run_pipeline():
    print("=== 1. EXTRACT ===")
    rows = fetch_all()
    save_raw(rows)

    print("\n=== 2. TRANSFORM ===")
    raw_df = load_raw()
    clean_df = clean(raw_df)
    save_processed(clean_df)

    print("\n=== 3. LOAD ===")
    df = load_clean_csv()
    load_to_sqlite(df)

    print("\n=== 4. VISUALIZE ===")
    viz_df = load_data()
    plot_evolution(viz_df)
    plot_monthly_average(viz_df)

    print("\nPipeline completo.")


if __name__ == "__main__":
    run_pipeline()