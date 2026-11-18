# Connext Media 3D AI 团队办公室

## 功能
- Three.js 3D 大头可爱角色办公室
- 总监室、会议室（BTC 预留）、开放工位、休息区、茶水间、法庭
- 实时状态显示（工作中 / 思考中 / 浏览 / 需要帮助 / 空闲 / 已完成）
- 昼夜切换、演示模式、手机触控支持
- 文件存储状态 + Token 鉴权上报接口

## 角色
- Grok（调度总监）
- COO、美术总监、设计师、影片生成师、影片剪辑师、写文案专员
- 2 名剧本脚本人员
- 6 名商品调查员
- 法庭：检察官 Claude、辩护律师 Claude、法官 Claude、12 名陪审员

## 本地运行
```bash
# 前端
cd office
python3 -m http.server 8080
# 打开 http://localhost:8080

# 后端（可选）
pip install flask flask-cors
python3 server.py
# API: http://localhost:5000/api/status
# 上报: POST /api/report  Header: Authorization: Bearer connext-media-secret-token-2026
# Body: {"id":"coo","status":"working","task":"提交法庭"}
```

## 上报示例
```bash
curl -X POST http://localhost:5000/api/report \
  -H "Authorization: Bearer connext-media-secret-token-2026" \
  -H "Content-Type: application/json" \
  -d '{"id":"grok","status":"working","task":"生成日报"}'
```

## 安全
- Token 鉴权
- 请求限流（30次/分钟/IP）
- 密钥通过环境变量管理（生产请修改 TOKEN）

## 公开部署建议
- 前端：Vercel / Netlify / GitHub Pages
- 后端：Railway / Render / Fly.io
- 将 status.json 持久化（或换 SQLite）
