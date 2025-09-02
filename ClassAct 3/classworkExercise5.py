def weighted_average(a, b, c):
    return float(a*0.3 + b*0.3 + c*0.4)

def main() -> None: 
    print(f"Weighted average: {weighted_average(82.5,91,77):.2f}")
    
main()