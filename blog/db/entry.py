#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    fragment = db.Column(db.Text) #内容片段, 用于主页显示
    status = db.Column(db.Integer, default=1) #完成：1, 失败0, 草稿:-1  （暂时无用）
    create_time = db.Column(db.DateTime, index=True, default=datetime.now())
    modify_time = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category = db.relationship('Category', backref=db.backref('entries', lazy='dynamic'), lazy='select')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    tag = db.relationship('Tag', secondary=tag_entry, backref=db.backref('entries', lazy='dynamic'))
    view_count = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Entry %r>' % self.title

    def __unicode__(self):
        return self.title
