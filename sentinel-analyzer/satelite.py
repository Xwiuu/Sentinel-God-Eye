import asyncio
import websockets
import redis.asyncio as redis

async def transmitir_alertas(websocket):
    print("🌐 [SATÉLITE] Novo Monitor God Eye Conectado!")
    
    # Conexão assíncrona blindada
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    pubsub = r.pubsub()
    await pubsub.subscribe('SENTINEL_GEO_STREAM')
    
    try:
        while True:
            # O timeout=0.1 faz ele escutar rápido e liberar o processador pro WebSocket não cair
            mensagem = await pubsub.get_message(ignore_subscribe_messages=True, timeout=0.1)
            
            if mensagem and mensagem['type'] == 'message':
                print("⚡ [SATÉLITE] Alerta recebido do Cérebro! Disparando laser pro Front-end...")
                await websocket.send(mensagem['data'])
                
            await asyncio.sleep(0.05) 
            
    except websockets.exceptions.ConnectionClosed:
        print("⚠️ [SATÉLITE] Monitor Desconectado.")
    finally:
        await pubsub.close()
        await r.aclose() # Desliga o motor suavemente

async def main():
    print("🛰️ Satélite Sentinel decolando... Escutando na porta 3001.")
    async with websockets.serve(transmitir_alertas, "localhost", 3001):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())