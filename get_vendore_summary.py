import sqlite3
import pandas as pd
import logging
import time
from ingest_db import ingest_db

logging.basicConfig(
    filename="logs/get_vendor_summary.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s - %(message)s",
    filemode="a"
)

def create_vendor_summary(conn):
    start = time.time()

    final_table = pd.read_sql_query("""
    WITH PurchaseSummary AS (
        SELECT
            p.VendorNumber,
            p.VendorName,
            p.Brand,
            p.Description,
            p.PurchasePrice,
            pp.Price AS ActualPrice,
            pp.Volume,
            SUM(p.Quantity) AS TotalPurchaseQuantity,
            SUM(p.Dollars) AS TotalPurchaseDollars
        FROM purchases p
        JOIN purchase_prices pp
            ON p.Brand = pp.Brand
        WHERE p.PurchasePrice > 0
        GROUP BY
            p.VendorNumber,
            p.VendorName,
            p.Brand,
            p.Description,
            p.PurchasePrice,
            pp.Price,
            pp.Volume
    ),

    SalesSummary AS (
        SELECT
            VendorNo,
            Brand,
            SUM(SalesQuantity) AS TotalSalesQuantity,
            SUM(SalesDollars) AS TotalSalesDollars,
            SUM(SalesPrice) AS TotalSalesPrice,
            SUM(ExciseTax) AS TotalExciseTax
        FROM sales
        GROUP BY VendorNo, Brand
    ),

    FreightSummary AS (
        SELECT
            VendorNumber,
            SUM(Freight) AS FreightCost
        FROM vendor_invoice
        GROUP BY VendorNumber
    )

    SELECT
        ps.VendorNumber,
        ps.VendorName,
        ps.Brand,
        ps.Description,
        ps.PurchasePrice,
        ps.ActualPrice,
        ps.Volume,
        ps.TotalPurchaseQuantity,
        ps.TotalPurchaseDollars,
        ss.TotalSalesQuantity,
        ss.TotalSalesDollars,
        ss.TotalSalesPrice,
        ss.TotalExciseTax,
        fs.FreightCost
    FROM PurchaseSummary ps
    LEFT JOIN SalesSummary ss
        ON ps.VendorNumber = ss.VendorNo
        AND ps.Brand = ss.Brand
    LEFT JOIN FreightSummary fs
        ON ps.VendorNumber = fs.VendorNumber
    ORDER BY ps.TotalPurchaseDollars DESC
    """, conn)

    logging.info(
        f"Vendor summary created in {round(time.time() - start, 2)} seconds"
    )
    return final_table


def clean_data(final_table):
    final_table['Volume'] = final_table['Volume'].astype(float)
    final_table.fillna(0, inplace=True)

    final_table['VendorName'] = final_table['VendorName'].str.strip()
    final_table['Description'] = final_table['Description'].str.strip()

    final_table['GrossProfit'] = (
        final_table['TotalSalesDollars'] - final_table['TotalPurchaseDollars']
    )
    final_table['ProfitMargin'] = (
        final_table['GrossProfit'] / final_table['TotalSalesDollars']
    ) * 100
    final_table['StockTurnover'] = (
        final_table['TotalSalesQuantity'] /
        final_table['TotalPurchaseQuantity']
    )
    final_table['SalesToPurchaseRatio'] = (
        final_table['TotalSalesDollars'] /
        final_table['TotalPurchaseDollars']
    )

    return final_table


if __name__ == "__main__":
    conn = sqlite3.connect("inventory.db")

    logging.info("Creating Vendor Summary Table...")
    final_table = create_vendor_summary(conn)
    logging.info(final_table.head())

    logging.info("Cleaning Data...")
    final_table = clean_data(final_table)
    logging.info(final_table.head())

    logging.info("Ingesting data...")
    ingest_db(final_table, "vendor_sales_summary", conn)

    logging.info("Completed successfully")
