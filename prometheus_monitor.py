from prometheus_api_client import PrometheusConnect, MetricsList, MetricSnapshotDataFrame, MetricRangeDataFrame
from datetime import datetime, timedelta
from prometheus_api_client.utils import parse_datetime
import matplotlib.pyplot as plt
import argparse
import numpy as np

def show_plot(metric_df: MetricSnapshotDataFrame) -> None:
    plt.figure(figsize=(10, 6))
    metric_df["value"].plot(marker='o', linestyle='-', title=f"Service: {metric_df["service"][0]}, Metric: {metric_df["__name__"][0]}", legend=True)

    plt.xlabel("Timestamp", fontsize=12)
    plt.ylabel("Value", fontsize=12)
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
    description="""WhiteBox monitoring of data_collector and server"""
    )

    parser.add_argument("-s", "--service",  type=str, help="specify the service you want to monitor")
    parser.add_argument("-m", "--metric",  type=str, help="specify the metric you are interested in")
    parser.add_argument("-r", "--range", type=int, help="specify the temporal range in minutes")
    parser.add_argument("port", type=str, help="specify the port of the prometheus server")

    args = parser.parse_args()

    prom = PrometheusConnect(url=f"http://127.0.0.1:{args.port}/", disable_ssl=True)

    #define labels
    start_time = f"{args.range}m" if args.range else (datetime.now() - timedelta(days=1))

    services = ["data_collector", "server"]
    metrics = ["update_time", "response_time_get_stock_price_average", "requests_count_total", "error_count_total"]
    
    metrics_data = []

    label_config = {"service": args.service} if args.service else None
    metric = args.metric if args.metric else ""

    if not args.service and not args.metric:
        for m in metrics:
            metrics_data.append(prom.get_metric_range_data(
                metric_name=m,
                label_config=label_config,
                start_time=start_time,
                chunk_size = timedelta(minutes=1)
            ))
    elif not args.metric:
        for m in metrics:
            metrics_data.append(prom.get_metric_range_data(
                metric_name=m,
                label_config=label_config,
                start_time=start_time,
                chunk_size = timedelta(minutes=1)
            ))
    elif not args.service:
        for s in services:
            metrics_data.append(prom.get_metric_range_data(
                metric_name=metric,
                label_config={"service": s},
                start_time=start_time,
                chunk_size = timedelta(minutes=1)
            ))
    else:
        metrics_data.append(prom.get_metric_range_data(
                metric_name=metric,
                label_config=label_config,
                start_time=start_time,
                chunk_size = timedelta(minutes=1)
            ))

    for metric_data in metrics_data:
        #translate the rusult in a dataframe
        try:
            metric_df = MetricSnapshotDataFrame(metric_data)
            print(metric_df)
            show_plot(metric_df)
        except Exception:
            continue 