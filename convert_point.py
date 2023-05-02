points = "39% 9%, 39% 20%, 44% 20%, 49% 22%, 52% 24%, 55% 28%, 58% 32%, 60% 37%, 61% 39%, 68% 36%, 65% 28%, 62% 22%, 58% 18%, 55% 15%, 49% 12%, 45% 10%"
x = points.split(",")
point_str = ""
for p in x:
    x_corr = float(p.split()[0].strip('%'))/100 * 1286
    y_corr = float(p.split()[1].strip('%'))/100 * 500
    point_str += str(x_corr) +","+ str(y_corr) + " "
print(point_str)
