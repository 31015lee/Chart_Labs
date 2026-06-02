# Chart Labs 배포 가이드

## 🚀 Streamlit Cloud로 배포 (추천 - 무료)

### 1단계: GitHub에 푸시
```bash
cd /workspaces/Chart_Labs
git add .
git commit -m "Deploy to Streamlit Cloud"
git push origin main
```

### 2단계: Streamlit Cloud 계정 만들기
- https://streamlit.io/cloud 접속
- GitHub 계정으로 로그인

### 3단계: 앱 배포
1. Streamlit Cloud 대시보드에서 "New app" 클릭
2. Repository: Chart_Labs 선택
3. Branch: main 선택
4. Main file path: app.py 입력
5. "Deploy!" 클릭

**배포 완료!** 몇 초 후에 공개 URL이 생성됩니다.

---

## 📦 Docker로 배포 (고급)

### Dockerfile 생성
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

### 배포 플랫폼 옵션:
- **Railway**: https://railway.app
- **Render**: https://render.com
- **AWS EC2/ECS**
- **Google Cloud Run**
- **Azure App Service**

---

## ✅ 배포 확인
- 배포 후 공개 URL로 접속 가능
- 모든 사용자가 URL만으로 접속 가능
- Streamlit Cloud에서 자동 SSL 지원

---

## 🔗 더 알아보기
- Streamlit 공식 배포 문서: https://docs.streamlit.io/streamlit-cloud/deploy-your-app
