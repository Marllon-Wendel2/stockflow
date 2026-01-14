def process_stock(items):
    if not items:
        raise ValueError("Lista vazia")

    return {
        "processed": len(items),
        "status": "ok"
    }