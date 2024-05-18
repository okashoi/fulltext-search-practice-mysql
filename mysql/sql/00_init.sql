create table `works` (
  `id` int unsigned not null primary key comment '作品ID',
  `title` varchar(255) not null comment '作品名'
) comment '作品';

create table `sentences` (
  `work_id` int unsigned not null comment '作品ID',
  `position` int unsigned not null comment '作中において何番目の文か（数値は 1 から開始）',
  `content` text not null comment '文の内容',
  primary key (`work_id`, `position`),
  foreign key (`work_id`) references `works` (`id`) on delete cascade on update cascade
) comment '文';
