
var PLANE_LENGTH = 34;  //货架板面长度
var PLANE_WIDTH = 55;   //货架板面宽度
var PLANE_HEIGHT = 2;   //货架板面高度
var HOLDER_LENGTH = 2;  //支架长度
var HOLDER_WIDTH = 2;   //支架宽度
var HOLDER_HEIGHT = 25; //支架高度
var LAYER_NUM = 3;      //货架层数
var COLUMN_NUM = 1;     //货架每层列数
var BOX_SIZE = 25;      //货物的大小(立方体)

//货架数组
var shelf_list = new Array();
shelf_list.push({StorageZoneId:'A',shelfId:'A1',shelfName:'SectionA1',x:-1000,y:27,z:-500});
shelf_list.push({StorageZoneId:'A',shelfId:'A2',shelfName:'SectionA2',x:-900,y:27,z:-500});
shelf_list.push({StorageZoneId:'A',shelfId:'A3',shelfName:'SectionA3',x:-800,y:27,z:-500});
shelf_list.push({StorageZoneId:'A',shelfId:'A4',shelfName:'SectionA4',x:-700,y:27,z:-500});
shelf_list.push({StorageZoneId:'A',shelfId:'A5',shelfName:'SectionA5',x:-600,y:27,z:-500});

shelf_list.push({StorageZoneId:'B',shelfId:'B1',shelfName:'SectionB1',x:-300,y:27,z:-500});
shelf_list.push({StorageZoneId:'B',shelfId:'B2',shelfName:'SectionB2',x:-200,y:27,z:-500});
shelf_list.push({StorageZoneId:'B',shelfId:'B3',shelfName:'SectionB3',x:-100,y:27,z:-500});
shelf_list.push({StorageZoneId:'B',shelfId:'B4',shelfName:'SectionB4',x:0,y:27,z:-500});
shelf_list.push({StorageZoneId:'B',shelfId:'B5',shelfName:'SectionB5',x:100 ,y:27,z:-500});

shelf_list.push({StorageZoneId:'C',shelfId:'C1',shelfName:'SectionB1',x:400,y:27,z:-500});
shelf_list.push({StorageZoneId:'C',shelfId:'C2',shelfName:'SectionB2',x:500,y:27,z:-500});
shelf_list.push({StorageZoneId:'C',shelfId:'C3',shelfName:'SectionB3',x:600,y:27,z:-500});
shelf_list.push({StorageZoneId:'C',shelfId:'C4',shelfName:'SectionB4',x:700,y:27,z:-500});
shelf_list.push({StorageZoneId:'C',shelfId:'C5',shelfName:'SectionB5',x:800 ,y:27,z:-500});

shelf_list.push({StorageZoneId:'D',shelfId:'D1',shelfName:'SectionD1',x:-1000,y:27,z:-50});
shelf_list.push({StorageZoneId:'D',shelfId:'D2',shelfName:'SectionD2',x:-900,y:27,z:-50});
shelf_list.push({StorageZoneId:'D',shelfId:'D3',shelfName:'SectionD3',x:-800,y:27,z:-50});
shelf_list.push({StorageZoneId:'D',shelfId:'D4',shelfName:'SectionD4',x:-700,y:27,z:-50});
shelf_list.push({StorageZoneId:'D',shelfId:'D5',shelfName:'SectionD5',x:-600,y:27,z:-50});

shelf_list.push({StorageZoneId:'E',shelfId:'E1',shelfName:'SectionE1',x:-300,y:27,z:-50});
shelf_list.push({StorageZoneId:'E',shelfId:'E2',shelfName:'SectionE2',x:-200,y:27,z:-50});
shelf_list.push({StorageZoneId:'E',shelfId:'E3',shelfName:'SectionE3',x:-100,y:27,z:-50});
shelf_list.push({StorageZoneId:'E',shelfId:'E4',shelfName:'SectionE4',x:0,y:27,z:-50});
shelf_list.push({StorageZoneId:'E',shelfId:'E5',shelfName:'SectionE5',x:100 ,y:27,z:-50});

shelf_list.push({StorageZoneId:'F',shelfId:'F1',shelfName:'SectionF1',x:400,y:27,z:-50});
shelf_list.push({StorageZoneId:'F',shelfId:'F2',shelfName:'SectionF2',x:500,y:27,z:-50});
shelf_list.push({StorageZoneId:'F',shelfId:'F3',shelfName:'SectionF3',x:600,y:27,z:-50});
shelf_list.push({StorageZoneId:'F',shelfId:'F4',shelfName:'SectionF4',x:700,y:27,z:-50});
shelf_list.push({StorageZoneId:'F',shelfId:'F5',shelfName:'SectionF5',x:800 ,y:27,z:-50});

shelf_list.push({StorageZoneId:'G',shelfId:'G1',shelfName:'SectionG1',x:-1000,y:27,z:400});
shelf_list.push({StorageZoneId:'G',shelfId:'G2',shelfName:'SectionG2',x:-900,y:27,z:400});
shelf_list.push({StorageZoneId:'G',shelfId:'G3',shelfName:'SectionG3',x:-800,y:27,z:400});
shelf_list.push({StorageZoneId:'G',shelfId:'G4',shelfName:'SectionG4',x:-700,y:27,z:400});
shelf_list.push({StorageZoneId:'G',shelfId:'G5',shelfName:'SectionG5',x:-600,y:27,z:400});

shelf_list.push({StorageZoneId:'H',shelfId:'H1',shelfName:'SectionH1',x:-300,y:27,z:400});
shelf_list.push({StorageZoneId:'H',shelfId:'H2',shelfName:'SectionH2',x:-200,y:27,z:400});
shelf_list.push({StorageZoneId:'H',shelfId:'H3',shelfName:'SectionH3',x:-100,y:27,z:400});
shelf_list.push({StorageZoneId:'H',shelfId:'H4',shelfName:'SectionH4',x:0,y:27,z:400});
shelf_list.push({StorageZoneId:'H',shelfId:'H5',shelfName:'SectionH5',x:100 ,y:27,z:400});

shelf_list.push({StorageZoneId:'I',shelfId:'I1',shelfName:'SectionI1',x:400,y:27,z:400});
shelf_list.push({StorageZoneId:'I',shelfId:'I2',shelfName:'SectionI2',x:500,y:27,z:400});
shelf_list.push({StorageZoneId:'I',shelfId:'I3',shelfName:'SectionI3',x:600,y:27,z:400});
shelf_list.push({StorageZoneId:'I',shelfId:'I4',shelfName:'SectionI4',x:700,y:27,z:400});
shelf_list.push({StorageZoneId:'I',shelfId:'I5',shelfName:'SectionI5',x:800 ,y:27,z:400});


function GET_PLANE_LENGTH(){
  return PLANE_LENGTH;
}

function GET_PLANE_WIDTH(){
  return PLANE_WIDTH;
}

function GET_PLANE_HEIGHT(){
  return PLANE_HEIGHT;
}

function GET_HOLDER_LENGTH(){
  return HOLDER_LENGTH;
}

function GET_HOLDER_WIDTH(){
  return HOLDER_WIDTH;
}

function GET_HOLDER_HEIGHT(){
  return HOLDER_HEIGHT;
}

function GET_LAYER_NUM(){
  return LAYER_NUM;
}

function GET_COLUMN_NUM(){
  return COLUMN_NUM;
}

function GET_BOX_SIZE(){
  return BOX_SIZE;
}

function GET_SHELF_LIST(){
  return shelf_list;
}
