//
//  ZhCommandFilterImpl.swift
//  MyVoiceIdentifier
//
//  Created by justin on 2018/10/25.
//  Copyright © 2018年 tw.com.habook. All rights reserved.
//

import Foundation

public class ZhCommandFilter: CommandFilter {
    /*
     //第二階指令
     private static final Set<String> ACTION_TEXT_SET_SECOND_STAGE = new HashSet<String>(Arrays.asList(
     ACTION_TEXT_START,
     ACTION_TEXT_RESUME,
     ACTION_TEXT_STOP,
     ACTION_TEXT_ADD_SCORE,
     ACTION_TEXT_SNAPSHOT
     ));
     */
    
    //啟始關鍵字
    let commandPrefixSet: Set = [
            "小豆", "豆子", "小到", "想到", "小偷", "小刀", "少到", "少斗", "抢道", "吵到"
        ]
    
    //指令 - 第一階 - 正規式 - 挑人
    let actionRegPickArray = [
            "挑.个", "选.个", "条.个",
            "挑.位", "选.位", "条.位"
        ]
    
    //指令 - 第一階 - 正規式 - 計分板
    let actionRegScoreArray = [
            "加.分", "加.份", "家.分", "家.份",
            "加[0-9]+分", "加[0-9]+份", "家[0-9]+分", "家[0-9]+份",
            "\\+[0-9]+分"
        ]
    
    //指令 - 第一階 - 關鍵字 - 即問即答
    let actionTextIrsSet: Set = [
            "即问即答",
            "及问题答", "几问题打", "就问题大", "及问题打", "去问题他", "进问题打", "及问题的",
            "急忘记打", "机忘记打", "期忘记打", "去忘记打", "趣忘记打", "集忘记打",
            "星期忘记", "星期问题",
            "去玩趣打"
        ]
    
    //指令 - 第一階 - 關鍵字 - 即問即答 - 前半
    let actionTextIrsComboPrefixSet: Set = [
            "基本", "几万", "积分", "机关", "指纹", "期望", "请问", "急问", "去问", "期问", "期万"
        ]
    
    //指令 - 第一階 - 關鍵字 - 即問即答 - 後半
    let actionTextIrsComboPostfixSet: Set = [
            "鸡蛋", "击倒", "局长", "知道", "几张", "几道", "祈祷", "机打", "寄到", "寄道", "及党", "去打", "即答"
        ]
    
    //指令 - 第一階 - 關鍵字 - 搶權
    let actionTextSnatchSet: Set = [
            "抢权", "强权", "抢群", "抢圈", "产权", "强群", "掌权"
        ]
    
    //指令 - 第一階 - 關鍵字 - 統計與排行
    let actionTextStaticSet: Set = [
            "显示", "显四", "显市", "呈现"
        ]
    
    //指令 - 第一階 - 關鍵字 - 翻牌
    let actionTextFlopSet: Set = [
            "翻牌"
        ]
    
    //指令 - 第一階 - 關鍵字 - 計時器
    let actionTextCountDownSet: Set = [
            "倒数", "倒数计时", "计时"
        ]
    
    //指令 - 第一階 - 關鍵字 - 挑人
    let actionTextPickSet: Set = [
            "条", "挑", "挑出", "挑选", "选出"
        ]
    
    //指令 - 第二階 - 關鍵字
    let actionTextStart = "开始";
    let actionTextResume = "继续";
    let actionTextStop = "暂停";
    let actionTextAddScore = "给分";
    let actionTextSnapshot = "截图";
    
    //參數 - 挑人 - 單位
    let paramTextPickUnitSet: Set = ["位", "个"]
    
    //參數 - 統計與排行
    let paramTextStaticBarSet: Set = [
            "长条图", "成调图", "强调图", "场调图"
        ]
    let paramTextStaticGroupBarSet : Set = [
            "分组长条图", "分组成调图", "分组强调图", "分组场调图"
        ]
    let paramTextStaticCircle = "圆饼图"
    let paramTextStaticGroupCircle = "分组圆饼图"
    
    //參數 - 計時器 - 單位
    let paramTextCountDownUnitSet: Set = [
            "秒", "秒钟"
        ]
    
    /*
    //參數 - 計分板 - 加分
    let paramTextScoreSet: Set = [
            "加1分",  "加11分", "加一分", "加十一分",
            "加2分",  "加12分", "加二分", "加十二分",
            "加3分",  "加13分", "加三分", "加十三分",
            "加4分",  "加14分", "加四分", "加十四分",
            "加5分",  "加15分", "加五分", "加十五分",
            "加6分",  "加16分", "加六分", "加十六分",
            "加7分",  "加17分", "加七分", "加十七分",
            "加8分",  "加18分", "加八分", "加十八分",
            "加9分",  "加19分", "加九分", "加十九分",
            "加10分", "加20分", "加十分", "加二十分",
            "加两分"
        ]
    */
    
    //參數修飾 - 挑人 - 回答選項 - 類型1
    let paramDecorationPickChooseType1TextSet: Set = [
            "选1",  "选择1",  "答1",  "回答1",  "答案1",  "选项1",
            "选2",  "选择2",  "答2",  "回答2",  "答案2",  "选项2",
            "选3",  "选择3",  "答3",  "回答3",  "答案3",  "选项3",
            "选4",  "选择4",  "答4",  "回答4",  "答案4",  "选项4",
            "选5",  "选择5",  "答5",  "回答5",  "答案5",  "选项5",
            "选6",  "选择6",  "答6",  "回答6",  "答案6",  "选项6",
            "选7",  "选择7",  "答7",  "回答7",  "答案7",  "选项7",
            "选8",  "选择8",  "答8",  "回答8",  "答案8",  "选项8",
            "选9",  "选择9",  "答9",  "回答9",  "答案9",  "选项9",
            "选一", "选择一", "答一", "回答一", "答案一", "选项一",
            "选二", "选择二", "答二", "回答二", "答案二", "选项二",
            "选三", "选择三", "答三", "回答三", "答案三", "选项三",
            "选四", "选择四", "答四", "回答四", "答案四", "选项四",
            "选五", "选择五", "答五", "回答五", "答案五", "选项五",
            "选六", "选择六", "答六", "回答六", "答案六", "选项六",
            "选七", "选择七", "答七", "回答七", "答案七", "选项七",
            "选八", "选择八", "答八", "回答八", "答案八", "选项八",
            "选九", "选择九", "答九", "回答九", "答案九", "选项九"
        ]
    
    //參數修飾 - 挑人 - 回答選項 - 類型2
    let paramDecorationPickChooseType2RegSet: Set = [
            "第.个", "第[0-9]个", "的.个", "的[0-9]个"
        ]
    /*
     private static final Set<String> PARAM_DECORATION_TEXT_SET_PICK_CHOOSE_TYPE2 = new HashSet<>(Arrays.asList(
     "第1个", "第2个", "第3个", "第4个", "第5个", "第6个", "第7个", "第8个", "第9个",
     "第一个", "第二个", "第三个", "第四个", "第五个", "第六个", "第七个", "第八个", "第九个"
     ));
     */
    
    //參數修飾 - 挑人 - 回答正確
    let paramDecorationPickCorrectTextSet: Set = [
            "打对", "答对", "大队", "回答正确", "选择正确"
        ]
    
    //參數修飾 - 挑人 - 回答錯誤
    let paramDecorationPickIncorrectTextSet: Set = [
            "打错", "答错", "回答错误", "选择错误"
        ]
    
    //參數修飾 - 挑人 - 換答案
    let paramDecorationPickChangeTextSet: Set = [
            "换答案", "更改答案", "改答案", "答案有变", "答案有改", "变更答案"
        ]
    
    //參數修飾 - 計分板 - 每一組
    let paramDecorationScoreEachGroupSet: Set = [
            "每1组", "每一组"
        ]
    
    //參數修飾 - 計分板 - 第x組
    let paramDecorationScoreGroupSet: Set = [
            "1组",  "11组", "一组", "十一组",
            "2组",  "12组", "二组", "十二组",
            "3组",  "13组", "三组", "十三组",
            "4组",  "14组", "四组", "十四组",
            "5组",  "15组", "五组", "十五组",
            "6组",  "16组", "六组", "十六组",
            "7组",  "17组", "七组", "十七组",
            "8组",  "18组", "八组", "十八组",
            "9组",  "19组", "九组", "十九组",
            "10组", "20组", "十组", "二十组"
        ]
    
    //數字
    let chineseNumber = ["一","二","三","四","五","六","七","八","九"];
    let chineseNumberUnit = ["十","百","千","万","亿"];
    let chineseReplaceArr = [
            "两":"二"
        ]
    
    //過濾啟始關鍵字
    public func filterPrefix(segArr: [String]?) -> [String]? {
        //必須以「小豆」開始，所以至少有一個以上的切詞
        guard let segArr = segArr, segArr.count >= 2 else {
            return nil
        }
        
        var hasPrefix = false
        var commandStringArray = [String]()
        for seg in segArr {
            if self.commandPrefixSet.contains(seg) {
                //找到「小豆」後，hasPrefix 設為 true
                hasPrefix = true
                
                //for 有兩個「小豆」時，重設指令處理
                commandStringArray = [String]()
                
                continue
            }
            
            //在命令語句片斷中，加入
            if hasPrefix {
                commandStringArray.append(seg)
            }
        }
        
        //沒有以「小豆」開頭，略過
        if !hasPrefix {
            return nil
        }
        
        //除了「小豆」，沒有講其它的字，略過
        if commandStringArray.count < 1 {
            return nil
        }
        
        return commandStringArray
    }
    
    //搜尋指令 - 常規式 - 第一階
    public func filterActionReg(segArr: [String]?) -> String? {
        guard let segArr = segArr else {
            return nil
        }
        
        for seg in segArr {
            //挑人
            for regex in actionRegPickArray {
                if checkRegMatch(seg: seg, regex: regex) {
                    return SpeechCommand.ActionTypeConstant.actionTypePick
                }
            }
            
            //計分板
            for regex in actionRegScoreArray {
                if checkRegMatch(seg: seg, regex: regex) {
                    return SpeechCommand.ActionTypeConstant.actionTypeScore
                }
            }
        }
        
        return nil
    }
    
    //搜尋指令 - 指令的 index
    public func filterActionIndex(segArr: [String]?) -> Int? {
        guard let segArr = segArr, segArr.count >= 1 else {
            return nil
        }
        
        //先搜尋第一階指令
        for index in 0...segArr.count-1 {
            let seg = segArr[index]
            
            var segNext = seg
            if index != segArr.count-1 {
                segNext = segArr[index+1]
            }
            
            let actionFirstStage = self.convertActionFirstStage(actionText: seg, actionTextNext: segNext)
            if actionFirstStage != SpeechCommand.ActionTypeConstant.actionTypeUndefined {
                return index
            }
        }
        
        //再搜尋第二階指令
        for index in 0...segArr.count {
            let seg = segArr[index]
            let actionSecondStage = self.convertActionSecondStage(actionText: seg)
            if actionSecondStage != nil {
                return index
            }
        }
        
        return SpeechCommand.actionIndexNotFound
    }
    
    //搜尋指令 - 轉換指令 - 第一階
    public func convertActionFirstStage(actionText: String?, actionTextNext: String?) -> String? {
        guard let actionText = actionText, actionText.count > 0 else {
            return SpeechCommand.ActionTypeConstant.actionTypeUndefined
        }
        
        if actionTextIrsSet.contains(actionText) {
            return SpeechCommand.ActionTypeConstant.actionTypeIRS
        } else if let actionTextNext = actionTextNext {
            if actionTextIrsComboPrefixSet.contains(actionText) && actionTextIrsComboPostfixSet.contains(actionTextNext) {
                return SpeechCommand.ActionTypeConstant.actionTypeIRS
            }
        }
        
        if actionTextSnatchSet.contains(actionText) {
            return SpeechCommand.ActionTypeConstant.actionTypeSnatch
        }
        
        if actionTextStaticSet.contains(actionText) {
            return SpeechCommand.ActionTypeConstant.actionTypeStatic
        }
        
        if actionTextFlopSet.contains(actionText) {
            return SpeechCommand.ActionTypeConstant.actionTypeFlop
        }
        
        if actionTextCountDownSet.contains(actionText) {
            return SpeechCommand.ActionTypeConstant.actionTypeCountDown
        }
        
        if actionTextPickSet.contains(actionText) {
            return SpeechCommand.ActionTypeConstant.actionTypePick
        }
        
        return SpeechCommand.ActionTypeConstant.actionTypeUndefined
    }
    
    //搜尋指令 - 轉換指令 - 第二階
    public func convertActionSecondStage(actionText: String?) -> String? {
        guard let actionText = actionText, actionText.count > 0 else {
            return SpeechCommand.ActionTypeConstant.actionTypeUndefined
        }
        
        if actionText == actionTextStart {
            return SpeechCommand.ActionTypeConstant.actionTypeStart
        }
        
        if actionText == actionTextResume {
            return SpeechCommand.ActionTypeConstant.actionTypeResume
        }
        
        if actionText == actionTextStop {
            return SpeechCommand.ActionTypeConstant.actionTypeStop
        }
        
        if actionText == actionTextAddScore {
            return SpeechCommand.ActionTypeConstant.actionTypeAddScore
        }
        
        if actionText == actionTextSnapshot {
            return SpeechCommand.ActionTypeConstant.actionTypeSnapshot
        }
        
        return SpeechCommand.ActionTypeConstant.actionTypeUndefined
    }
    
    //搜尋參數 - 挑人
    public func filterPickParam(segArr: [String]?) -> Int! {
        guard let segArr = segArr, segArr.count > 0 else {
            return SpeechCommand.ParamConstant.paramUndefined
        }
        
        for seg in segArr {
            if seg.count < 2 { //以"個"或"位"為結束的中文字，前面有數字，所以是兩個字以上
                continue
            }
            
            for unit in paramTextPickUnitSet {
                if !seg.hasSuffix(unit) {
                    continue
                }
                
                let subseg = String(seg.prefix(seg.count-1))
                let result = toInt(rawText: subseg)
                if result < 0 {
                    return SpeechCommand.ParamConstant.paramUndefined
                }
                return result
            }
        }
        
        return SpeechCommand.ParamConstant.paramUndefined
    }
    
    //搜尋參數 - 統計與排行
    public func filterStaticParam(segArr: [String]?) -> Int! {
        guard let segArr = segArr, segArr.count > 0 else {
            return SpeechCommand.ParamConstant.paramUndefined
        }
        
        for seg in segArr {
            if paramTextStaticBarSet.contains(seg) {
                return SpeechCommand.ParamConstant.paramStaticBar
            }
            
            if paramTextStaticGroupBarSet.contains(seg) {
                return SpeechCommand.ParamConstant.paramStaticGroupBar
            }
            
            if paramTextStaticCircle == seg {
                return SpeechCommand.ParamConstant.paramStaticCircle
            }
            
            if paramTextStaticGroupCircle == seg {
                return SpeechCommand.ParamConstant.paramStaticGroupCircle
            }
        }
        
        return SpeechCommand.ParamConstant.paramUndefined
    }
    
    //搜尋參數 - 計時器
    public func filterCountDownParam(segArr: [String]?) -> Int! {
        guard let segArr = segArr, segArr.count > 0 else {
            return SpeechCommand.ParamConstant.paramUndefined
        }
        
        //過濾秒數 - 找到「秒」前一個切詞，轉成數字後回傳
        for index in 0...(segArr.count-1) {
            if index == 0 {
                continue
            }
            
            let seg = segArr[index]
            for subunit in paramTextCountDownUnitSet {
                if seg != subunit {
                    continue
                }
                
                let prevSeg = segArr[index-1]
                let temp = toInt(rawText: prevSeg)
                if temp >= 0 {
                    return temp
                }
            }
        }
        
        return SpeechCommand.ParamConstant.paramUndefined
    }
    
    //搜尋參數 - 計分板
    public func filterScoreParam(segArr: [String]?) -> Int! {
        guard let segArr = segArr, segArr.count > 0 else {
            return SpeechCommand.ParamConstant.paramUndefined
        }
        
        for seg in segArr {
            for regex in actionRegScoreArray {
                if !checkRegMatch(seg: seg, regex: regex) {
                    continue
                }
                
                let subseg = String(seg.prefix(seg.count-1).suffix(seg.count-2))
                let temp = toInt(rawText: subseg)
                if temp >= 0 {
                    return temp
                }
            }
        }
        
        return SpeechCommand.ParamConstant.paramUndefined
    }
    
    //搜尋參數修飾 - 挑人
    //  - 最後一個字轉成數字
    //  - 中間的字轉成數字
    //  - 回答正確、回答錯誤、變更答案
    public func filterPickParamDecoration(segArr: [String]?) -> Int! {
        guard let segArr = segArr, segArr.count > 0 else {
            return SpeechCommand.ParamDecorationConstant.paramDecorationUndefined
        }
        
        for seg in segArr {
            var ans = -1
            
            //選擇選項 - 最後一個字轉成數字
            //  - "选1",  "选择1",  "答1",  "回答1",  "答案1",  "选项1"
            if paramDecorationPickChooseType1TextSet.contains(seg) {
                ans = toInt(rawText: String(seg.suffix(1)))
            }
            
            //選擇選項 - 中間轉成數字
            //  - "第.个", "第[0-9]个", "的.个", "的[0-9]个"
            for regex in paramDecorationPickChooseType2RegSet {
                if checkRegMatch(seg: seg, regex: regex) {
                    ans = toInt(rawText: String(seg.prefix(2).suffix(1)))
                }
            }
            
            //選擇選項 - 回傳
            if ans > 0 {
                switch ans {
                case 1:
                    return SpeechCommand.ParamDecorationConstant.paramDecorationPickAns1
                case 2:
                    return SpeechCommand.ParamDecorationConstant.paramDecorationPickAns2
                case 3:
                    return SpeechCommand.ParamDecorationConstant.paramDecorationPickAns3
                case 4:
                    return SpeechCommand.ParamDecorationConstant.paramDecorationPickAns4
                case 5:
                    return SpeechCommand.ParamDecorationConstant.paramDecorationPickAns5
                case 6:
                    return SpeechCommand.ParamDecorationConstant.paramDecorationPickAns6
                case 7:
                    return SpeechCommand.ParamDecorationConstant.paramDecorationPickAns7
                case 8:
                    return SpeechCommand.ParamDecorationConstant.paramDecorationPickAns8
                case 9:
                    return SpeechCommand.ParamDecorationConstant.paramDecorationPickAns9
                default:
                    break;
                }
            }
            
            //回答正確
            if paramDecorationPickCorrectTextSet.contains(seg) {
                return SpeechCommand.ParamDecorationConstant.paramDecorationPickAnsCorrect
            }
            
            //回答錯誤
            if paramDecorationPickIncorrectTextSet.contains(seg) {
                return SpeechCommand.ParamDecorationConstant.paramDecorationPickAnsIncorrect
            }
            
            //變更答案
            if paramDecorationPickChangeTextSet.contains(seg) {
                return SpeechCommand.ParamDecorationConstant.paramDecorationPickAnsChange
            }
        }
        
        return SpeechCommand.ParamDecorationConstant.paramDecorationUndefined
    }
    
    //搜尋參數修飾 - 計分板
    //  - "1组",  "11组", "一组", "十一组"
    public func filterScoreParamDecoration(segArr: [String]?) -> Int! {
        guard let segArr = segArr, segArr.count > 0 else {
            return SpeechCommand.ParamDecorationConstant.paramDecorationUndefined
        }
        
        for seg in segArr {
            //每一組
            for regex in paramDecorationScoreEachGroupSet {
                if checkRegMatch(seg: seg, regex: regex) {
                    return SpeechCommand.ParamDecorationConstant.paramDecorationScoreGroupEach
                }
            }
            
            //第幾組
            if paramDecorationScoreGroupSet.contains(seg) {
                let subseg = String(seg.prefix(seg.count-1))
                let temp = toInt(rawText: subseg)
                switch temp {
                case 1:
                    return SpeechCommand.ParamDecorationConstant.paramDecorationScoreGroup1
                case 2:
                    return SpeechCommand.ParamDecorationConstant.paramDecorationScoreGroup2
                case 3:
                    return SpeechCommand.ParamDecorationConstant.paramDecorationScoreGroup3
                case 4:
                    return SpeechCommand.ParamDecorationConstant.paramDecorationScoreGroup4
                case 5:
                    return SpeechCommand.ParamDecorationConstant.paramDecorationScoreGroup5
                case 6:
                    return SpeechCommand.ParamDecorationConstant.paramDecorationScoreGroup6
                case 7:
                    return SpeechCommand.ParamDecorationConstant.paramDecorationScoreGroup7
                case 8:
                    return SpeechCommand.ParamDecorationConstant.paramDecorationScoreGroup8
                case 9:
                    return SpeechCommand.ParamDecorationConstant.paramDecorationScoreGroup9
                case 10:
                    return SpeechCommand.ParamDecorationConstant.paramDecorationScoreGroup10
                case 11:
                    return SpeechCommand.ParamDecorationConstant.paramDecorationScoreGroup11
                case 12:
                    return SpeechCommand.ParamDecorationConstant.paramDecorationScoreGroup12
                case 13:
                    return SpeechCommand.ParamDecorationConstant.paramDecorationScoreGroup13
                case 14:
                    return SpeechCommand.ParamDecorationConstant.paramDecorationScoreGroup14
                case 15:
                    return SpeechCommand.ParamDecorationConstant.paramDecorationScoreGroup15
                case 16:
                    return SpeechCommand.ParamDecorationConstant.paramDecorationScoreGroup16
                case 17:
                    return SpeechCommand.ParamDecorationConstant.paramDecorationScoreGroup17
                case 18:
                    return SpeechCommand.ParamDecorationConstant.paramDecorationScoreGroup18
                case 19:
                    return SpeechCommand.ParamDecorationConstant.paramDecorationScoreGroup19
                case 20:
                    return SpeechCommand.ParamDecorationConstant.paramDecorationScoreGroup20
                default:
                    break
                }
            }
        }
        
        return SpeechCommand.ParamDecorationConstant.paramDecorationUndefined
    }
    
    //以正規表示式檢查字串
    private func checkRegMatch(seg: String, regex: String) -> Bool {
        do {
            let regex = try NSRegularExpression(pattern: regex)
            let results = regex.matches(in: seg,range: NSRange(seg.startIndex..., in: seg))
            let match = results.map {
                String(seg[Range($0.range, in: seg)!])
            }
            if match.count > 0 {
                return true
            }
        } catch let error {
            print("invalid regex: \(error.localizedDescription)")
        }
        
        return false
    }
    
    //將文字轉成 Int
    private func toInt(rawText: String?) -> Int {
        guard let rawText = rawText, rawText.count > 0 else {
            return -1
        }
        
        //嘗試直接轉成數字
        if isInt(text: rawText) {
            return Int(rawText)!
        }
        
        let rawTextLastSubString = String(rawText.suffix(1))
        
        //以國字的數字處理
        var result = 0
        var temp = 1 //存放一個單位的數字，如十萬
        var count = 0 //判斷是否有chArr
        for subChar in rawText {
            var isNumberUnit = true //判斷是否是 chArr
            var currentSubString = String(subChar)
            let isLast = (currentSubString == rawTextLastSubString)
            
            //置換
            for (search, replace) in chineseReplaceArr {
                if currentSubString != search {
                    continue
                }
                
                currentSubString = replace
                break
            }
            
            //非單位即數字
            for index in 0...chineseNumber.count-1 {
                if currentSubString != chineseNumber[index] {
                    continue
                }
            
                //添加下一個單位之前，先把上一個單位值添加到結果中
                if count != 0 {
                    result += temp
                    temp = 1
                    count = 0
                }
                
                //下標+1，就是對應的值
                temp = index + 1
                isNumberUnit = false
                break;
            }
            
            //單位 {"十"，"百"，"千"，"萬"，"億"}
            if isNumberUnit {
                for index in 0...chineseNumberUnit.count-1 {
                    if currentSubString != chineseNumberUnit[index] {
                        continue
                    }
                    
                    switch index {
                    case 0:
                        temp *= 10
                        break;
                    case 1:
                        temp *= 100
                        break;
                    case 2:
                        temp *= 1000
                    case 3:
                        temp *= 10000
                    case 4:
                        temp *= 100000000
                    default:
                        break;
                    }
                    count = count + 1
                }
            }
            
            //遍歷到最後一個字元
            if isLast {
                result += temp
            }
        }
        
        return result
    }
    
    //字串是否為 Int
    private func isInt(text: String) -> Bool {
        return Int(text) != nil
    }
}

