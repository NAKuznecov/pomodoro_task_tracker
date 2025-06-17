from typing import List, Annotated

from fastapi import APIRouter, status, Depends
from schema.s_task import STask
from dependency import get_tasks_repository, get_cache_repository, get_task_service
from repository import TaskRep, CacheTask
from service.task import TaskService

router = APIRouter(prefix="/task", tags=["task"])


@router.get(
    "/all",
    response_model=List[STask],
)
async def get_tasks(
        task_service: Annotated[TaskService, Depends(get_task_service)],
):
    return task_service.get_tasks()



@router.post(
    "/",
    response_model=STask,
)
async def create_task(
        task: STask,
        task_repo: Annotated[TaskRep, Depends(get_tasks_repository)],
        ):
    task_id = task_repo.create_task(task)
    task.id = task_id
    return task


@router.patch(
    "/{task_id}",
    response_model=STask,
)
async def patch_task(
        task_id: int,
        name: str,
        task_repo: Annotated[TaskRep, Depends(get_tasks_repository)],
):
    return task_repo.update_name(task_id, name)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_task(
        task_id: int,
        task_repo: Annotated[TaskRep, Depends(get_tasks_repository)],
):
    task_repo.delete_task(task_id)
    return {'message': 'deleted successfully'}
