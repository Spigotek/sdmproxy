from fastapi import APIRouter, HTTPException, Body, Path
from app.sdm_client import sdm_client
from app.utils.logger import logger
import json

def create_router(object_name: str, prefix: str, description: str):
    router = APIRouter(prefix=prefix, tags=[description])

    @router.post("/search")
    def search_items(payload: dict = Body(default={"attrs": "id,common_name"})):
        """
        Načíta zoznam objektov z SDM (GET_LIST).
        """
        try:
            attrs = payload.get("attrs", "id,common_name")
            logger.info(f"[{object_name.upper()}] Listing with attrs={attrs}")
            response = sdm_client.get(f"{object_name}?OP=GET_LIST&attrs={attrs}&size=100")

            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=f"SDM returned {response.status_code}")

            data = response.json()
            coll_key = f"collection_{object_name}"
            items = data.get(coll_key, {}).get(object_name, [])
            count = data.get(coll_key, {}).get("@COUNT", len(items))
            return {"object": object_name, "count": count, "items": items, "source": "SDM"}

        except Exception as e:
            logger.exception(f"[{object_name.upper()}] Error: {e}")
            raise HTTPException(status_code=500, detail=f"Nepodarilo sa načítať dáta ({object_name}): {str(e)}")

    @router.get("/get/{obj_id}")
    def get_item(obj_id: str = Path(...)):
        """
        Získa detail objektu z SDM (GET).
        """
        try:
            logger.info(f"[{object_name.upper()}] Fetching ID={obj_id}")
            response = sdm_client.get(f"{object_name}/{obj_id}")

            if response.status_code != 200:
                raise HTTPException(status_code=response.status_code, detail=f"SDM returned {response.status_code}")

            return {"object": object_name, "data": response.json(), "source": "SDM"}

        except Exception as e:
            logger.exception(f"[{object_name.upper()}] Error: {e}")
            raise HTTPException(status_code=500, detail=f"Nepodarilo sa načítať detail {object_name}: {str(e)}")

    @router.post("/create")
    def create_item(payload: dict = Body(...)):
        """
        Vytvorí nový objekt v SDM (POST).
        """
        try:
            logger.info(f"[{object_name.upper()}] Creating new item: {payload}")
            response = sdm_client.post(object_name, json=payload)

            if response.status_code not in [200, 201]:
                raise HTTPException(status_code=response.status_code, detail=f"SDM returned {response.status_code}")

            return {"object": object_name, "created": True, "data": response.json(), "source": "SDM"}

        except Exception as e:
            logger.exception(f"[{object_name.upper()}] Error: {e}")
            raise HTTPException(status_code=500, detail=f"Nepodarilo sa vytvoriť objekt {object_name}: {str(e)}")

    @router.put("/update/{obj_id}")
    def update_item(obj_id: str, payload: dict = Body(...)):
        """
        Aktualizuje existujúci objekt v SDM (PUT).
        """
        try:
            logger.info(f"[{object_name.upper()}] Updating ID={obj_id}: {payload}")
            response = sdm_client.put(f"{object_name}/{obj_id}", json=payload)

            if response.status_code not in [200, 204]:
                raise HTTPException(status_code=response.status_code, detail=f"SDM returned {response.status_code}")

            return {"object": object_name, "updated": True, "status": response.status_code}

        except Exception as e:
            logger.exception(f"[{object_name.upper()}] Error: {e}")
            raise HTTPException(status_code=500, detail=f"Nepodarilo sa aktualizovať {object_name}: {str(e)}")

    @router.delete("/delete/{obj_id}")
    def delete_item(obj_id: str):
        """
        Zmaže objekt v SDM (DELETE).
        """
        try:
            logger.info(f"[{object_name.upper()}] Deleting ID={obj_id}")
            response = sdm_client.delete(f"{object_name}/{obj_id}")

            if response.status_code not in [200, 204]:
                raise HTTPException(status_code=response.status_code, detail=f"SDM returned {response.status_code}")

            return {"object": object_name, "deleted": True, "status": response.status_code}

        except Exception as e:
            logger.exception(f"[{object_name.upper()}] Error: {e}")
            raise HTTPException(status_code=500, detail=f"Nepodarilo sa odstrániť {object_name}: {str(e)}")

    return router
