create table user
(
    ID   int unsigned auto_increment
        primary key,
    name tinytext null
);

create table probe
(

    keystroke json                     not null comment 'keystrokes JSON, it have a fixed size',
    userid    int unsigned             not null,
    keystrokesID      int unsigned auto_increment primary key comment 'keystrokesID',
    FA        int unsigned default '0' not null comment 'false acceptance',
    FR        int unsigned default '0' not null comment 'false rejection',
    constraint probe_user_ID_fk
        foreign key (userid) references user (ID)
            on update cascade on delete cascade
) comment 'users probes of the keystrokes'



