create table user
(
    ID   int unsigned auto_increment
        primary key,
    name tinytext null
);

create table probe
(

    userid    int unsigned             not null,
    keystrokeID      int unsigned auto_increment primary key comment 'keystrokesID',
    FA        int unsigned default '0' not null comment 'false acceptance',
    FR        int unsigned default '0' not null comment 'false rejection',
    GA        int unsigned default '0' not null comment 'genuine acceptance',
    GR        int unsigned default '0' not null comment 'genuine rejection',
    keystroke json                     not null comment 'keystrokes JSON, it have a fixed size',
    constraint probe_user_ID_fk
        foreign key (userid) references user (ID)
            on update cascade on delete cascade
) comment 'users probes of the keystrokes';


create table cold_start
(
    has_cold_start bool default true not null
);

insert into cold_start value (1);

