<!-- TransactionsPage.vue -->
<template>
  <div class="legal-container">
    <h1>特定商取引法に基づく表記</h1>

    <div class="legal-section">
      <h2>販売業者</h2>
      <p>Geneartweave</p>
    </div>

    <div class="legal-section">
      <h2>運営責任者</h2>
      <p>松枝 優弥</p>
    </div>

    <div class="legal-section">
      <h2>所在地</h2>
      <p>〒140-0013</p>
      <p>東京都品川区南大井６丁目３番１４号</p>
    </div>

    <div class="legal-section">
      <h2>連絡先</h2>
      <p>メールアドレス：contact@geneartweave.com</p>
    </div>

    <div class="legal-section">
      <h2>商品の販売価格</h2>
      <p>商品価格：3,000円（税込）</p>
      <p>※別途送料が必要な場合があります</p>
    </div>

    <div class="legal-section">
      <h2>支払い方法</h2>
      <p>クレジットカード決済（Stripe）</p>
      <ul>
        <li>VISA</li>
        <li>MasterCard</li>
        <li>American Express</li>
      </ul>
    </div>

    <div class="legal-section">
      <h2>商品の引き渡し時期</h2>
      <p>ご注文確認後、5-7営業日以内に発送いたします。</p>
      <p>※繁忙期や天候状況により遅延する場合があります</p>
    </div>

    <div class="legal-section">
      <h2>返品・キャンセルについて</h2>
      <p>
        商品の性質上（オーダーメイド商品のため）、原則として返品・キャンセルはお受けできません。
      </p>
      <p>ただし、以下の場合は返品・交換を承ります：</p>
      <ul>
        <li>商品到着時の破損・汚損があった場合</li>
        <li>商品に明らかな不良があった場合</li>
      </ul>
      <p>上記の場合、商品到着後7日以内にメールにてご連絡ください。</p>
    </div>
  </div>
</template>

<!-- PrivacyPolicy.vue -->
<template>
  <div class="legal-container">
    <h1>プライバシーポリシー</h1>

    <div class="legal-section">
      <h2>1. 収集する情報</h2>
      <p>当サービスでは、以下の情報を収集します：</p>
      <ul>
        <li>氏名</li>
        <li>配送先住所</li>
        <li>メールアドレス</li>
        <li>注文情報</li>
        <li>AIイラスト生成用プロンプト</li>
      </ul>
    </div>

    <div class="legal-section">
      <h2>2. 情報の利用目的</h2>
      <ul>
        <li>商品の配送</li>
        <li>代金の決済</li>
        <li>お問い合わせ対応</li>
        <li>サービスの品質向上</li>
        <li>新商品・サービスの開発</li>
      </ul>
    </div>

    <div class="legal-section">
      <h2>3. Stable Diffusionの使用について</h2>
      <p>当サービスでは、Stable Diffusionを使用してAIイラストを生成しています。</p>
      <p>以下の内容の画像生成は禁止されています：</p>
      <ul>
        <li>違法または公序良俗に反するもの</li>
        <li>他人の著作権を侵害するもの</li>
        <li>暴力的または過度に性的な表現を含むもの</li>
        <li>差別的な表現を含むもの</li>
      </ul>
    </div>

    <div class="legal-section">
      <h2>4. 情報の第三者提供</h2>
      <p>収集した個人情報は、以下の場合を除き第三者に提供することはありません：</p>
      <ul>
        <li>決済処理のためのStripeへの提供</li>
        <li>商品配送のための配送業者への提供</li>
        <li>法令に基づく場合</li>
      </ul>
    </div>

    <div class="legal-section">
      <h2>5. お問い合わせ</h2>
      <p>プライバシーポリシーに関するお問い合わせは、下記までご連絡ください：</p>
      <p>メールアドレス：contact@geneartweave.com</p>
    </div>
  </div>
</template>

<style scoped>
.legal-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
  line-height: 1.6;
}

h1 {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #eee;
}

.legal-section {
  margin-bottom: 2rem;
}

h2 {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1rem;
  color: #333;
}

p {
  margin-bottom: 1rem;
}

ul {
  list-style-type: disc;
  margin-left: 1.5rem;
  margin-bottom: 1rem;
}

li {
  margin-bottom: 0.5rem;
}
</style>
