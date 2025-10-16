from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.sdm_client import sdm_client
import requests

router = APIRouter(prefix="/api/attachments", tags=["attachments"])


@router.get("/{cr_id}")
def list_attachments(cr_id: str):
    """
    Zoznam príloh pre daný incident
    """
    resp = sdm_client.get(f"attachment?cr={cr_id}")
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()


@router.post("/{cr_id}")
def upload_attachment(cr_id: str, file: UploadFile = File(...), description: str = Form(None)):
    """
    Nahratie prílohy ku incidentu
    """
    url = f"{sdm_client.config.SDM_BASE_URL}/attachment"
    headers = sdm_client._get_headers()
    files = {
        "file": (file.filename, file.file, file.content_type)
    }
    data = {"description": description or "Uploaded via SDM Proxy", "cr": {"id": cr_id}}

    resp = requests.post(url, headers=headers, files=files, data=data)
    if resp.status_code not in (200, 201):
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()


@router.delete("/{attach_id}")
def delete_attachment(attach_id: str):
    """
    Vymazanie prílohy
    """
    resp = sdm_client.delete(f"attachment/{attach_id}")
    if resp.status_code not in (200, 204):
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return {"message": f"Attachment {attach_id} deleted."}
