# 📊 Real-Time Market Data & Portfolio Risk Analytics Platform

## Domain

Capital Markets · Portfolio Analytics · Risk Engineering

---

## 🚀 Project Overview

This project implements a **production-style, real-time market data and portfolio risk analytics platform** similar to systems used by trading desks and risk teams at banks, hedge funds, and fintech firms.

The platform ingests **streaming market prices**, aggregates them into intraday price bars, values portfolios in near real time, and computes **PnL and risk metrics** such as volatility, Value-at-Risk (VaR), and concentration exposure.

It demonstrates an **end-to-end data engineering workflow** combining streaming + batch processing with strong data quality and analytics modeling practices.

---

## 🧩 Business Problem

Financial institutions require **timely visibility into portfolio value and risk** to:

* Support trading and hedging decisions
* Monitor intraday exposure
* Enforce risk limits
* Produce end-of-day regulatory and management reports

Market data arrives continuously and must be:

* Ingested reliably
* Aggregated efficiently
* Reconciled with portfolio positions
* Validated for financial accuracy

This project simulates a **front-to-back analytics pipeline** used in real-world capital markets environments.

---

## 🏗️ Architecture Overview

**Hybrid Streaming + Batch Architecture**

```
Market Price Producer
      ↓
Kafka (Raw Market Prices)
      ↓
Spark Structured Streaming
      ↓
Bronze Layer (Tick-Level Prices)
      ↓
Spark Batch Aggregation
      ↓
Silver Layer (5-Minute Price Bars)
      ↓
Portfolio Valuation & Risk Engine
      ↓
PostgreSQL Warehouse (Gold)
      ↓
dbt Models & Finance Reports
```

---

## 🛠️ Technology Stack

**Streaming**

* Apache Kafka
* Spark Structured Streaming

**Processing**

* PySpark (Streaming + Batch)

**Orchestration**

* Apache Airflow

**Warehouse**

* PostgreSQL

**Transformation & Testing**

* dbt

**Storage**

* Parquet (Bronze / Silver layers)

**Infrastructure**

* Docker
* Linux shell scripting

**Languages**

* Python
* SQL

---

## 📡 Data Sources

### 1️⃣ Real-Time Market Data (Kafka)

Simulated tick-level prices for:

* Equities (e.g., AAPL, MSFT)
* ETFs
* FX pairs

Example event:

```json
{
  "symbol": "AAPL",
  "ts_event": "2025-09-24T14:32:10Z",
  "price": 189.42,
  "currency": "USD",
  "exchange": "NASDAQ",
  "volume": 1200
}
```

### 2️⃣ Reference & Position Data (Batch)

* Portfolio definitions
* Instrument master
* Daily positions (quantity, average cost)

---

## 🔄 Data Pipeline Design

### 🥉 Bronze Layer – Raw Market Data

* Ingests tick-level prices from Kafka
* Schema validation and deduplication
* Partitioned by trade date and symbol
* Checkpointing for fault tolerance

---

### 🥈 Silver Layer – Aggregated Price Bars

* Spark batch job runs every **5 minutes**
* Generates:

  * OHLC price bars
  * VWAP
* Normalizes timestamps and currencies
* Handles late-arriving data

**Example Output**

```
(symbol, window_start, open, high, low, close, vwap)
```

---

### 🥇 Gold Layer – Portfolio Valuation & Risk

Computed per portfolio:

* Market value
* Unrealized PnL
* Asset-level and portfolio-level exposure
* Rolling volatility
* Historical Value-at-Risk (95%)

---

## 📈 Financial Analytics Implemented

### Portfolio Valuation

* **Market Value** = Quantity × Close Price
* **Unrealized PnL** = (Close Price − Avg Cost) × Quantity

### Risk Metrics

* Historical Value-at-Risk (VaR, 95%)
* Rolling volatility (20-day)
* Concentration risk (single-asset exposure %)
* Maximum drawdown per portfolio

---

## 🗄️ Data Warehouse Design (PostgreSQL)

### Dimensions

* `dim_date`
* `dim_symbol`
* `dim_exchange`
* `dim_portfolio`

### Fact Tables

* `fact_price_bars`
* `fact_positions`
* `fact_portfolio_valuation`
* `fact_pnl_daily`
* `fact_risk_metrics`

⭐ Star schema optimized for finance analytics queries.

---

## ✅ dbt Models & Data Quality

* Modular dbt models for facts and dimensions
* Built-in tests:

  * `not_null`
  * `unique`
  * `relationships`

**Custom finance validations**

* Prices > 0

* Quantity ≠ 0

* Portfolio exposure reconciles to market value

* dbt documentation with full data lineage

---

## ⏱️ Orchestration (Airflow)

### DAG 1 – Intraday (Every 5 Minutes)

* Aggregate market prices
* Update silver price bars

### DAG 2 – End of Day

* Revalue portfolios
* Compute risk metrics
* Run dbt models and tests
* Export finance reports

Configured with retries, SLAs, and failure logging.

---

## 📊 Reporting Outputs

### 1️⃣ Daily Portfolio PnL Report

* Daily and month-to-date PnL
* Top gainers and losers
* Portfolio performance summary

### 2️⃣ Risk Exposure Report

* VaR by portfolio
* Concentration risk breaches
* Volatility rankings

---

## ⭐ Key Engineering Highlights

* End-to-end streaming + batch architecture
* Real-time market data ingestion with Kafka
* Spark-based financial aggregations
* Bronze–Silver–Gold data modeling
* Data quality enforcement using dbt
* Finance-grade analytics (PnL, VaR, exposure)

---

## 🎯 Why This Project Matters

This project demonstrates the ability to:

* Work with real-time financial market data
* Understand portfolio valuation and risk concepts
* Build production-grade data pipelines
* Design analytics systems used in capital markets

It goes beyond basic ETL and reflects **financial data engineering and analytics thinking**.

---

## 📌 Resume Highlights

* Built a real-time market data and portfolio analytics platform using Kafka, Spark, Airflow, and PostgreSQL
* Processed streaming market prices to compute intraday OHLC bars, portfolio valuation, and PnL metrics
* Designed Bronze–Silver–Gold architecture with Parquet storage and star-schema warehouse
* Implemented risk metrics including Value-at-Risk, volatility, and concentration exposure
* Applied dbt models and tests to ensure financial reporting accuracy

---

## 📎 Next Improvements

* Add real-time dashboards (Superset / Power BI)
* Introduce risk limit monitoring and alerts
* Expand to options and derivatives pricing
* Migrate warehouse to Snowflake or BigQuery

---

