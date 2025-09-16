from extensions import db

class Player(db.Model):
    __tablename__ = "players"
    id = db.Column(db.Integer, primary_key=True)

    # external player identity to link with other data sources
    ext_source = db.Column(db.String(32), nullable=False, default="sleeper")
    ext_id = db.Column(db.String(64), nullable=False)


    full_name = db.Column(db.String(200), nullable=False, index=True)
    position = db.Column(db.String(50))
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"))
    birth_date = db.Column(db.Date)
    height_in = db.Column(db.Integer)
    weight_lb = db.Column(db.Integer)

    __table_args__ = (db.UniqueConstraint("ext_source", "ext_id", name="_ext_source_ext_id_uc"),)
    
    team = db.relationship("Team", back_populates="players")

    def to_dict(self):
        return {
            "id": self.id,
            "ext_source": self.ext_source,
            "ext_id": self.ext_id,
            "full_name": self.full_name,
            "position": self.position,
            "team": self.team.code if self.team else None,
            "birth_date": self.birth_date.isoformat() if self.birth_date else None,
            "height_in": self.height_in,
            "weight_lb": self.weight_lb,
        }


class Team(db.Model):
  __tablename__ = "teams"
  id = db.Column(db.Integer, primary_key=True)
  code = db.Column(db.String(10), unique=True, index=True)
  name = db.Column(db.String(120))

  players = db.relationship("Player", back_populates="team")