from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database_management import Mysql_Method_Api
import os
from dotenv import load_dotenv
load_dotenv()  # This is to load the environment variables from the .env file


# 创建 FastAPI 实例
app = FastAPI()

# 加载环境变量
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

# 创建数据库管理实例
db_manager = Mysql_Method_Api(db_host, db_user, db_password, db_name)

# 预订模型
class Reservation(BaseModel):
    guest_phone_number: str
    guest_name: str
    num_of_guest: int
    reservation_date: str
    reservation_time: str
    table_unique_ID: int

# 创建预订路由
@app.post("/reservations/")
def make_reservation(reservation: Reservation):
    result = db_manager.make_reservations(
        reservation.guest_phone_number, reservation.guest_name,
        reservation.num_of_guest, reservation.reservation_date,
        reservation.reservation_time, reservation.table_unique_ID
    )
    if result:
        return {"message": "Reservation successful"}
    else:
        raise HTTPException(status_code=400, detail="Error in reservation")

# 取消预订路由
@app.delete("/reservations/{phone_number}")
def cancel_reservation(phone_number: str):
    db_manager.cancel_reservation_by_phone_number(phone_number)
    return {"message": "Reservation cancelled"}

# 获取可用桌子路由
@app.get("/tables/available")
def get_available_tables():
    available_tables = db_manager.check_available_tables()
    if available_tables:
        return {"tables": available_tables}
    else:
        raise HTTPException(status_code=404, detail="No available tables")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Reservation System API"}


# 运行 FastAPI 服务器
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.4.0", port=8000)
