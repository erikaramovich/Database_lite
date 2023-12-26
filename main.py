from models import *
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

# Create an in-memory SQLite database and initialize the schema
engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)

# Create a session to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Instantiate the FastAPI application
app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/sites/', response_model=int)
def create_site(site: ArchaeologicalSite, db: Session = Depends(get_db)):
    db.add(site)
    db.commit()
    db.refresh(site)
    return site.id

@app.get('/sites/', response_model=List[ArchaeologicalSite])
def read_sites(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(ArchaeologicalSite).offset(skip).limit(limit).all()

@app.get('/sites/{site_id}', response_model=ArchaeologicalSite)
def read_site(site_id: int, db: Session = Depends(get_db)):
    site = db.query(ArchaeologicalSite).filter(ArchaeologicalSite.id == site_id).first()
    if site is None:
        raise HTTPException(status_code=404, detail='Site not found')
    return site

@app.put('/sites/{site_id}', response_model=ArchaeologicalSite)
def update_site(site_id: int, updated_site: ArchaeologicalSite, db: Session = Depends(get_db)):
    db_site = db.query(ArchaeologicalSite).filter(ArchaeologicalSite.id == site_id).first()
    if db_site is None:
        raise HTTPException(status_code=404, detail='Site not found')
    db_site.name = updated_site.name
    db_site.location = updated_site.location
    db_site.period = updated_site.period
    db_site.specialization = updated_site.specialization
    db.commit()
    db.refresh(db_site)
    return db_site

@app.delete('/sites/{site_id}', response_model=dict)
def delete_site(site_id: int, db: Session = Depends(get_db)):
    db_site = db.query(ArchaeologicalSite).filter(ArchaeologicalSite.id == site_id).first()
    if db_site is None:
        raise HTTPException(status_code=404, detail='Site not found')
    db.delete(db_site)
    db.commit()
    return {'detail': 'Site deleted'}

