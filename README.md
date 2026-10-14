# tornado-flask
tornado flask 模板


# 运行MariaDB
```bash
docker run -d --name my_mariadb -v $(pwd)/datadir:/var/lib/mysql -e MARIADB_ROOT_PASSWORD=*** -e MYSQL_DATABASE=sales -e MYSQL_USER=sales -e MYSQL_PASSWORD=*** -p 3306:3306 -d mariadb:11.8.2

# 连接DB
mysql -h localhost -P 3306 -u root -p
```

# 变更表格
```bash
//初始化迁移仓库（如果尚未初始化）自动创建所有表
flask db init
//二次更新表, 如果migrate文件丢失，可删除表 alembic_version后，执行下面的步骤
flask db migrate -m "update sales models"
//如果已经执行过上一步，已经生成migrations.version 文件，则只用执行upgrade
flask db upgrade
```
