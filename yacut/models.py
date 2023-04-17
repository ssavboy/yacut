from datetime import datetime

from flask import url_for

from . import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(db.String, nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    def to_dict(self):
        return dict(
            original=self.original,
            short=url_for(
                'redirect_view',
                short=self.short,
                _external=True
            )
        )
    
    def from_dict(self, data):
        for key in ['url', 'custom_id']:
            if key in data: setattr(self, key, data[key])
