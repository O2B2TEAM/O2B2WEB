db연결

JOB/ app.py 에서 login,회원가입 기능 추가

cradle-to-grave/job ai이력서, 인재찾기, ai인터뷰 기능 추가

client = MongoClient("mongodb+srv://test:1234@cluster.ct8weib.mongodb.net/o2b2data?retryWrites=true&w=majority")
db = client["o2b2data"]

유저 로그인 정보 ->  user 컬렉션,

유저 이력서 관련 정보 -> resume_user 컬렉션

본 코드는 vs코드에서 적용됩니다. 
여러 라이브러리를 다운받아야 코드실행 가능할거에요

#api_key값은 계속 변경
llm = ChatOpenAI(api_key="sk-proj-uVJsV6efcMYXnhRlCq8OT3BlbkFJVNdTzPJoe1AgASexvfAO") 
