from main import app

#최초 실행파일(?)은 __name__변수에 __main__이 설정되며 해당 서버가 유일함을 증명한다.
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)

#git test