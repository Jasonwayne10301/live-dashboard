from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.auth import get_db, get_current_active_user, get_current_superuser
from app.core.simulator import simulator
from app.schemas.server import ServerCreate, ServerOut
from app.models.server import ServerConfig

router = APIRouter(prefix="/servers", tags=["Servers"])


@router.get("/", response_model=list[ServerOut])
async def list_servers(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    result = await db.execute(
        select(ServerConfig).where(ServerConfig.is_active is True)
    )
    return result.scalars().all()


@router.post("/", response_model=ServerOut, status_code=status.HTTP_201_CREATED)
async def create_server(
    server: ServerCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_superuser)
):
    result = await db.execute(
        select(ServerConfig).where(ServerConfig.name == server.name)
    )
    existing = result.scalars().first()
    if existing:
        raise HTTPException(status_code=400, detail="Server with that name already exists")

    db_server = ServerConfig(**server.model_dump())
    db.add(db_server)
    await db.commit()
    await db.refresh(db_server)
    await simulator.reload_servers()
    return db_server


@router.put("/{server_id}", response_model=ServerOut)
async def update_server(
    server_id: int,
    server: ServerCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_superuser)
):
    result = await db.execute(
        select(ServerConfig).where(ServerConfig.id == server_id)
    )
    db_server = result.scalars().first()
    if not db_server:
        raise HTTPException(status_code=404, detail="Server not found")

    for key, value in server.model_dump().items():
        setattr(db_server, key, value)

    db.add(db_server)
    await db.commit()
    await db.refresh(db_server)
    await simulator.reload_servers()
    return db_server


@router.delete("/{server_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_server(
    server_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_superuser)
):
    result = await db.execute(
        select(ServerConfig).where(ServerConfig.id == server_id)
    )
    db_server = result.scalars().first()
    if not db_server:
        raise HTTPException(status_code=404, detail="Server not found")

    db_server.is_active = False
    db.add(db_server)
    await db.commit()
    await simulator.reload_servers()
    return None
