
### 启动服务
```bash
# 开发环境
uvicorn app.main:app --reload
# or
ENV=dev python -m app.main
# or 
python -m app.main

# 生产环境
ENV=prod python -m app.main
```
#### 环境变量
- `ENV`：指定运行环境，可选值为 `dev`（开发环境）、`prod`（生产环境）和 `test`（测试环境）。默认值为 `dev`。

### 访问API文档
- 开发环境：[http://localhost:8000/docs](http://localhost:8000/docs)
- 生产环境：[http://localhost:8000/docs](http://localhost:8000/docs)
