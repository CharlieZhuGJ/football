# !/usr/bin/env python
# -*- coding:utf-8 -*-

"""
数据库配置
"""

T_PARSER_RULE = """
CREATE TABLE IF NOT EXISTS `ParserRule` (
    `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
    `ruleName` char(150) NOT NULL,
    `source` char(150) NOT NULL,
    `sampleLog` longtext NOT NULL,
    `rules` longtext NOT NULL,
    `status` tinyint(4) NOT NULL DEFAULT '0',
    `usageCount` smallint(6) NOT NULL DEFAULT '0',
    `filters` text,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""



#
# Agent主机组
#
T_AGENT_HOST_GROUP = """
CREATE TABLE IF NOT EXISTS `AgentGroup` (
  `id` char(40) NOT NULL,
  `name` text NOT NULL,
  `status` tinyint(1) NOT NULL DEFAULT 1,
  `description` text,
  `whitelist` text,
  `blacklist` text,
  `createTime` datetime DEFAULT now(),
  `latestUpdateTime` datetime DEFAULT now(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""



table_list = [T_PARSER_RULE, T_AGENT_HOST_GROUP]

table_names = ['ParserRule', 'AgentGroup']

ADMIN_ID = u"f5a08cb056c539d76f373bbc94458e39"
SECURIT_ID = u"f5a08cb056c539d76f373bbc94458e38"
AUDIT_ID = u"f5a08cb056c539d76f373bbc94458e37"
DEFAULT_PWD = u"e10adc3949ba59abbe56e057f20f883e"
DEFAULT_LOGGROUP_ID = u"fe5b7f96-443a-11e7-a467-000c29253e90"

THIRD_APPS = [{"appId": "AnyShare",
               "appSecret": "XJ2S93CF",
               "appName": "AnyShare",
               "status": 0,
               "config": {"signExpireTime": 300}}]


