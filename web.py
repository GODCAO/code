from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64


plt.rcParams['font.family'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

app = Flask(__name__)


# 词库
FORBIDDEN_WORDS = {"吃", "垃圾", "党不好", "草"}

# 问卷数据
survey_data = []


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # 获取用户提交的数据
        q1 = request.form.getlist("q1")
        q2 = request.form.getlist("q2")
        q3 = request.form.getlist("q3")
        q4 = request.form.get("q4")
        q4_reason = request.form.get("q4_reason")

        # 过滤敏感词
        if any(word in q4_reason for word in FORBIDDEN_WORDS):
            return "输入包含敏感词，请重新输入！"

        # 将数据存储到列表 (简单示例)
        survey_data.append({
            "q1": q1,
            "q2": q2,
            "q3": q3,
            "q4": q4,
            "q4_reason": q4_reason
        })

        return redirect(url_for("success"))

    return render_template("index.html")
@app.route("/success")
def success():
    # 渲染提交成功页面
    return render_template("success.html")


@app.route("/stats", methods=["GET"])
def stats():
    # 使用 app.app_context() 上下文管理器
    with app.app_context():

        # 将查询结果转换为 DataFrame
        df = pd.DataFrame(survey_data)


        # 统计数据
        q1_counts = df["q1"].explode().value_counts().reindex(["1.1", "1.2", "1.3", "1.4", "1.5"], fill_value=0)
        q2_counts = df["q2"].explode().value_counts().reindex(["2.1", "2.2", "2.3", "2.4", "2.5", "2.6", "2.7", "2.8"],
                                                              fill_value=0)
        q3_counts = df["q3"].explode().value_counts().reindex(["3.1", "3.2", "3.3", "3.4", "3.5"], fill_value=0)
        q4_counts = df["q4"].value_counts().reindex(["4.1", "4.2", "4.3", "4.4", "4.5"], fill_value=0)

        # 绘制图表
        plt.figure(figsize=(10, 5))
        q1_counts.plot(kind="bar")
        plt.title("问题 1 统计结果")
        plt.xlabel("选项")
        plt.ylabel("次数")
        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        q1_image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        plt.close()

        plt.figure(figsize=(10, 5))
        q2_counts.plot(kind="bar")
        plt.title("问题 2 统计结果")
        plt.xlabel("选项")
        plt.ylabel("次数")
        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        q2_image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        plt.close()

        plt.figure(figsize=(10, 5))
        q3_counts.plot(kind="bar")
        plt.title("问题 3 统计结果")
        plt.xlabel("选项")
        plt.ylabel("次数")
        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        q3_image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        plt.close()

        plt.figure(figsize=(10, 5))
        q4_counts.plot(kind="bar")
        plt.title("问题 4 统计结果")
        plt.xlabel("选项")
        plt.ylabel("次数")
        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        q4_image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        plt.close()

    # 渲染统计页面
    return render_template("stats.html",
                           q1_image_base64=q1_image_base64,
                           q2_image_base64=q2_image_base64,
                           q3_image_base64=q3_image_base64,
                           q4_image_base64=q4_image_base64)


if __name__ == "__main__":
    app.run(debug=True)
