import time
import json
import logging
import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from typing import Callable, Dict, Any, Optional

# ロガーの設定
logger = logging.getLogger("api")

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    HTTPリクエスト/レスポンスの詳細をログに記録するミドルウェア
    構造化されたJSON形式でログを出力します
    """
    
    def __init__(
        self, 
        app: ASGIApp, 
        log_level: int = logging.INFO,
        exclude_paths: Optional[list] = None,
        exclude_methods: Optional[list] = None
    ):
        super().__init__(app)
        self.log_level = log_level
        self.exclude_paths = exclude_paths or ["/health", "/metrics"]
        self.exclude_methods = exclude_methods or ["OPTIONS"]
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # リクエストIDを生成
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # リクエストパスがログ除外対象か確認
        if any(request.url.path.startswith(path) for path in self.exclude_paths):
            return await call_next(request)
            
        # リクエストメソッドがログ除外対象か確認
        if request.method in self.exclude_methods:
            return await call_next(request)
        
        # リクエスト開始時間
        start_time = time.time()
        
        # クライアント情報
        client_host = request.client.host if request.client else "unknown"
        client_port = request.client.port if request.client else "unknown"
        
        # ヘッダー情報
        headers = dict(request.headers)
        # 機密情報をマスク
        if "authorization" in headers:
            headers["authorization"] = "Bearer [REDACTED]"
        if "cookie" in headers:
            headers["cookie"] = "[REDACTED]"
            
        # リクエスト情報をログに記録
        request_log = {
            "request_id": request_id,
            "client_ip": client_host,
            "client_port": client_port,
            "method": request.method,
            "path": request.url.path,
            "query_params": str(request.query_params),
            "headers": headers,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # リクエストボディの取得（オプション）
        # リクエストボディを読み取ると元のリクエストハンドラでは読めなくなるため、通常は本番環境では無効にする
        # try:
        #     body = await request.body()
        #     if body:
        #         request_log["body"] = body.decode("utf-8")
        # except Exception:
        #     request_log["body"] = "Could not parse body"
            
        logger.log(self.log_level, f"Request received: {json.dumps(request_log)}")
        
        # レスポンス処理
        try:
            response = await call_next(request)
            
            # 処理時間計算
            process_time = time.time() - start_time
            
            # レスポンス情報
            response_log = {
                "request_id": request_id,
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "process_time_ms": round(process_time * 1000, 2),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # ステータスコードに基づいてログレベルを調整
            log_level = self.log_level
            if response.status_code >= 500:
                log_level = logging.ERROR
            elif response.status_code >= 400:
                log_level = logging.WARNING
                
            logger.log(log_level, f"Response sent: {json.dumps(response_log)}")
            
            return response
            
        except Exception as e:
            # 例外情報
            error_log = {
                "request_id": request_id,
                "error": str(e),
                "error_type": e.__class__.__name__,
                "process_time_ms": round((time.time() - start_time) * 1000, 2),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            logger.error(f"Exception occurred: {json.dumps(error_log)}")
            raise 