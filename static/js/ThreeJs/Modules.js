
//模型材质信息
var planeMat, RackMat, RackMat2, CargoMat, LineMat, RollTexture, RollMat;
//库区信息
var storageZoneSize = 0, storageZoneList = [];
//货架信息
var shelfSize = 0, shelfList = [];
//货位信息
var storageUnitSize = 0, storageUnitList = [];
//货物信息
var cargoSize = 0, cargoList = [], CargosExist;

//创建库区对象
function storageZone(StorageZoneId,StorageZoneName,
                     coordinateX,coordinateZ,
                     width,length,
                     textColor,fontSize,textposition)
{
    this.StorageZoneId=StorageZoneId;
    this.StorageZoneName=StorageZoneName;
    this.coordinateX=coordinateX;
    this.coordinateZ=coordinateZ;
    this.width=width;
    this.length=length;
    this.textColor=textColor;
    this.fontSize=fontSize;
    this.textposition=textposition;
}

//根据库区编码获取库区对象
function getStorageZoneById(StorageZoneId) {
    for(var i = 0; i < storageZoneSize; i++){
        if(storageZoneList[i].StorageZoneId == StorageZoneId){
            return storageZoneList[i];
        }
    }
}

//创建货架对象
function shelf(storageZoneId, shelfId, shelfName,
               planeLength , planeWidth , planeHeight ,
               holderLength , holderWidth , holderHeight ,
               positionX , positionY , positionZ ,
               layerNum , columnNum)
{
    this.storageZoneId=storageZoneId;
    this.shelfId=shelfId;
    this.shelfName=shelfName;
    this.planeLength=planeLength;
    this.planeWidth=planeWidth;
    this.planeHeight=planeHeight;
    this.holderLength=holderLength;
    this.holderWidth=holderWidth;
    this.holderHeight=holderHeight;
    this.positionX=positionX;
    this.positionY=positionY;
    this.positionZ=positionZ;
    this.layerNum=layerNum;
    this.columnNum=columnNum;
}

//根据货架编码获取货架对象
function getShelfById(shelfId) {
    for(var i = 0; i < shelfSize; i++){
        if(shelfList[i].shelfId == shelfId){
            return shelfList[i];
        }
    }
}

//创建货位对象
function storageUnit(storageZoneId, shelfId, shelfName,
               inLayerNum , inColumnNum ,
               positionX , positionY , positionZ, storageUnitId)
{
    this.storageZoneId=storageZoneId;
    this.shelfId=shelfId;
    this.shelfName=shelfName;
    this.inLayerNum=inLayerNum;
    this.inColumnNum=inColumnNum;
    this.positionX=positionX;
    this.positionY=positionY;
    this.positionZ=positionZ;
    this.storageUnitId=storageUnitId;
}

//根据货架ID、层数、列数获取货位对象
function getStorageUnitById(shelfId,inLayerNum,inColumnNum) {
    for(var i = 0; i < storageUnitSize; i++){
        if(storageUnitList[i].shelfId == shelfId && storageUnitList[i].inLayerNum == inLayerNum && storageUnitList[i].inColumnNum == inColumnNum){
            return storageUnitList[i];
        }
    }
}

//根据库位编码获取货位对象
function getStorageUnitByUnitId(storageUnitId) {
    for(var i = 0; i < storageUnitSize; i++){
        if(storageUnitList[i].storageUnitId == storageUnitId){
            return storageUnitList[i];
        }
    }
}

//创建货物对象
function cargo(batchNo, prodBatchNo, inBatchNo,
               matId, matClassId, matName,
               qty, qtyUom, qtyUom2,
               warehouseId, storageZoneId, storageUnitId,
               positionX , positionY , positionZ,
               length , width , height)
{
    this.batchNo=batchNo;
    this.prodBatchNo=prodBatchNo;
    this.inBatchNo=inBatchNo;
    this.matId=matId;
    this.matClassId=matClassId;
    this.matName=matName;
    this.qtyUom=qtyUom;
    this.qtyUom2=qtyUom2;
    this.warehouseId=warehouseId;
    this.storageZoneId=storageZoneId;
    this.storageUnitId=storageUnitId;
    this.positionX=positionX;
    this.positionY=positionY;
    this.positionZ=positionZ;
    this.length=length;
    this.width=width;
    this.height=height;
}

/** 初始化材质信息 */
function initMat() {
    planeMat = new THREE.MeshLambertMaterial();
    RackMat = new THREE.MeshLambertMaterial();
    RackMat2 = new THREE.MeshPhongMaterial({color:0x1C86EE});
    CargoMat = new THREE.MeshLambertMaterial();
    LineMat = new THREE.MeshLambertMaterial();
    RollMat = new THREE.MeshLambertMaterial();

    new THREE.TextureLoader().load( '/static/js/ThreeJs/images/plane.png', function( map ) {
        planeMat.map = map;
        planeMat.transparent = true;
        planeMat.opacity = 0.8;
        planeMat.needsUpdate = true;
    } );
    new THREE.TextureLoader().load( "/static/js/ThreeJs/images/rack.png", function( map ) {
        RackMat.map = map;
        RackMat.needsUpdate = true;
    } );
    new THREE.TextureLoader().load( "/static/js/ThreeJs/images/box.png", function( map ) {
        CargoMat.map = map;
        CargoMat.needsUpdate = true;
    } );
    new THREE.TextureLoader().load( "/static/js/ThreeJs/images/line.png", function( map ) {
        LineMat.map = map;
        LineMat.needsUpdate = true;
    } );
    RollTexture = new THREE.TextureLoader().load( "/static/js/ThreeJs/images/biaoyu.png", function( map ) {
        RollMat.map = map;
        RollMat.needsUpdate = true;
        RollMat.transparent = true;
        RollMat.side = THREE.DoubleSide;
    } );
    RollTexture.wrapS = THREE.RepeatWrapping;
    RollTexture.wrapT=THREE.RepeatWrapping;
}

//endregion

//region 滚动的物体
function addRollPlane(scene) {
    var geometry = new THREE.PlaneGeometry( 400, 20 );
    var obj = new THREE.Mesh( geometry, RollMat );
    obj.position.set(0,150,-690);
    scene.add( obj );
}
//endregion

//region 矩形区域
function addPlane(x,z,width,length,scene) {
    var lineWidth = 8;
    var geometry = new THREE.PlaneGeometry( lineWidth, length );
    var obj = new THREE.Mesh( geometry, LineMat );
    obj.position.set(x,1.5,z);
    obj.rotation.x = -Math.PI / 2.0;
    var obj2 = obj.clone();
    obj2.translateX(width);

    var geometry2 = new THREE.PlaneGeometry( lineWidth, width );
    var obj3 = new THREE.Mesh( geometry2, LineMat );
    obj3.position.set(x+width/2,1.5,z-length/2+lineWidth/2);
    obj3.rotation.x = -Math.PI / 2.0;
    obj3.rotation.z = -Math.PI / 2.0;
    var obj4 = obj3.clone();
    obj4.translateX(length-lineWidth);

    var group = new THREE.Group();
    group.add(obj);
    group.add(obj2);
    group.add(obj3);
    group.add(obj4);
    group.translateX(-width/2);
    scene.add( group );
}
//endregion

//region 库区
/** 放置虚线框区域和库区名称 */
function addArea(x,z,width,length,scene,name,textColor,font_size,textposition) {
    addPlane(x,z,width,length,scene);

    new THREE.FontLoader().load('/static/js/ThreeJs/FZYaoTi_Regular.json',function(font){
        ////加入立体文字
        var text= new THREE.TextGeometry(name.split("$")[1],{
            // 设定文字字体
            font:font,
            //尺寸
            size:font_size,
            //厚度
            height:0.01
        });
        text.computeBoundingBox();
        //3D文字材质
        var m = new THREE.MeshStandardMaterial({color:"#" + textColor});
        var mesh = new THREE.Mesh(text,m)
        if(textposition == "左对齐"){
            mesh.position.x = x - width/2 + 10;
        }else if(textposition == "居中"){
            mesh.position.x = x - 15;
        }else if(textposition == "右对齐"){
            mesh.position.x = x + width/2 - 60;
        }
        mesh.position.y = 1.3;
        mesh.position.z = z + length/2 - 20;
        mesh.rotation.x = -Math.PI / 2.0;
        scene.add(mesh);
    });
}
//endregion

//region 货架货位

/** 放置单层货架 */
/** x,y,z 整个模型在场景中的位置 */
/** plane_x,plane_y,plane_z 货架板面的长高宽 */
/** holder_x,holder_y,holder_z 货架支架的长高宽 */
/** scene,name,num 要添加的场景,货架的名字,单层货架的库位数量 */
function addRack(x,y,z,plane_x,plane_y,plane_z,holder_x,holder_y,holder_z,scene,name,num) {
    var plane = new THREE.BoxGeometry( plane_x, plane_y, plane_z/num );
    var gz = [];
    for(var i = 0; i < num; i++){
        gz.push( z + plane_z/num/2 + (plane_z/num)*i );
        var obj = new THREE.Mesh( plane, RackMat );
        obj.position.set(x , y, gz[i]) ;
        var msg = name+"$"+(GET_COLUMN_NUM() - i);

        var storageUnitId = msg.split("$")[1] + "$" + msg.split("$")[3] + "$" + msg.split("$")[4];

        //添加货位
        var storageUnit_obj = new storageUnit(msg.split("$")[0],
            msg.split("$")[1],
            msg.split("$")[2],
            msg.split("$")[3],
            msg.split("$")[4],
            x, y, gz[i], storageUnitId);
        storageUnitList.push(storageUnit_obj);
        storageUnitSize++;

        var Unit = getStorageUnitById(msg.split("$")[1],msg.split("$")[3],msg.split("$")[4]);
        obj.name = "Location"+"$"+Unit.storageUnitId;
        scene.add(obj);
    }

    var holder = new THREE.BoxGeometry( holder_x, holder_y, holder_z );
    var obj2 = new THREE.Mesh( holder, RackMat2, 0 );
    var obj3 = new THREE.Mesh( holder, RackMat2, 0 );
    var obj4 = new THREE.Mesh( holder, RackMat2, 0 );
    var obj5 = new THREE.Mesh( holder, RackMat2, 0 );

    obj2.position.set(x-plane_x/2+holder_x/2,y-holder_y/2-plane_y/2,z+holder_z/2);
    obj3.position.set(x+plane_x/2-holder_x/2,y-holder_y/2-plane_y/2,z+holder_z/2);
    obj4.position.set(x-plane_x/2+holder_x/2,y-holder_y/2-plane_y/2,z+plane_z-holder_z/2);
    obj5.position.set(x+plane_x/2-holder_x/2,y-holder_y/2-plane_y/2,z+plane_z-holder_z/2);
    scene.add(obj2);scene.add(obj3);scene.add(obj4);scene.add(obj5);
}

/** 放置一叠货架 */
/** stack_num 货架的叠数 */
function addStackOfRack(x,y,z,plane_x,plane_y,plane_z,holder_x,holder_y,holder_z,scene,name,num,stack_num) {
    for(var i = 0; i < stack_num; i++){
        addRack(x,y*(i+1),z,plane_x,plane_y,plane_z,holder_x,holder_y,holder_z,scene,name+"$"+(i+1),num);
    }
}

/** 根据3D库图货架配置表添加货架 */
function addShelf(scene) {
    var shelf_list = GET_SHELF_LIST();
    shelfSize = shelf_list.length;
    for(var i = 0; i < shelfSize; i++){
        var shelf_obj = new shelf(shelf_list[i].StorageZoneId,
            shelf_list[i].shelfId,
            shelf_list[i].shelfName,
            GET_PLANE_LENGTH(),GET_PLANE_WIDTH(),GET_PLANE_HEIGHT(),
            GET_HOLDER_LENGTH(),GET_HOLDER_WIDTH(),GET_HOLDER_HEIGHT(),
            shelf_list[i].x,
            shelf_list[i].y,
            shelf_list[i].z,
            GET_LAYER_NUM(),GET_COLUMN_NUM());
        shelfList.push(shelf_obj);
    }

    for(var i = 0;i < shelfSize; i++){
        addStackOfRack(shelfList[i].positionX,shelfList[i].positionY,shelfList[i].positionZ,shelfList[i].planeLength,shelfList[i].planeHeight,shelfList[i].planeWidth,shelfList[i].holderLength,shelfList[i].holderHeight,shelfList[i].holderWidth,scene,shelfList[i].storageZoneId+"$"+shelfList[i].shelfId+"$"+shelfList[i].shelfName,shelfList[i].columnNum,shelfList[i].layerNum);
    }
}

//region 货物
/** 放置单个货物 */
function addCargo(x,y,z,box_x,box_y,box_z,scene,name) {
    var geometry = new THREE.BoxGeometry( box_x, box_y, box_z );
    var obj = new THREE.Mesh( geometry, CargoMat );
    obj.position.set(x,y,z);
    obj.name = name;
    scene.add(obj);
}

/** 添加单个货位上的货物 */
function addOneUnitCargos(shelfId,inLayerNum,inColumnNum,scene,n,a) {
    var storageUnit = getStorageUnitById(shelfId,inLayerNum,inColumnNum);
    var shelf = getShelfById(shelfId);
    var storageUnitid = storageUnit.storageUnitId;
    var x = storageUnit.positionX;
    var y = storageUnit.positionY + GET_BOX_SIZE()/2 + shelf.planeHeight/2;
    var z = storageUnit.positionZ;
    addCargo(x,y,z,GET_BOX_SIZE(),GET_BOX_SIZE(),GET_BOX_SIZE(),scene, n+"    Amount: "+a+"          Location:  $"+storageUnitid)
}
//endregion
