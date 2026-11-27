/* MedBook — UI enhancements (vanilla JS, без фреймворков и AJAX).
   Всё работает как прогрессивное улучшение: без JS страницы остаются рабочими. */
(function () {
  'use strict';

  var ICON_EYE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/></svg>';
  var ICON_EYE_OFF = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 3l18 18"/><path d="M10.6 5.1A10.6 10.6 0 0 1 12 5c6.4 0 10 7 10 7a17.6 17.6 0 0 1-3.2 4.1M6.6 6.6C3.7 8.4 2 12 2 12s3.6 7 10 7a9.7 9.7 0 0 0 5.4-1.6"/><path d="M9.9 9.9a3 3 0 0 0 4.2 4.2"/></svg>';
  var ICON_STAR = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.8l2.8 5.7 6.3.9-4.6 4.4 1.1 6.3L12 17.1l-5.6 3 1.1-6.3L2.9 9.4l6.3-.9L12 2.8Z"/></svg>';

  function $all(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

  /* 1. Мобильное меню */
  function initNav() {
    var toggle = document.querySelector('[data-nav-toggle]');
    var nav = document.getElementById('site-nav');
    if (!toggle || !nav) return;
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      nav.classList.toggle('is-open', !open);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('is-open')) {
        toggle.setAttribute('aria-expanded', 'false');
        nav.classList.remove('is-open');
        toggle.focus();
      }
    });
  }

  /* 2. Флеш-сообщения: закрытие и автоскрытие успешных */
  function dismiss(el) {
    el.classList.add('is-leaving');
    setTimeout(function () { el.remove(); }, 260);
  }
  function initFlashes() {
    $all('.flash').forEach(function (flash) {
      var btn = flash.querySelector('.flash__close');
      if (btn) btn.addEventListener('click', function () { dismiss(flash); });
      if (flash.classList.contains('flash--success') || flash.classList.contains('flash--info')) {
        var timer = setTimeout(function () { dismiss(flash); }, 6000);
        flash.addEventListener('mouseenter', function () { clearTimeout(timer); });
      }
    });
  }

  /* 3. Подтверждение необратимых действий: <form data-confirm="Текст"> */
  function initConfirm() {
    document.addEventListener('submit', function (e) {
      var form = e.target;
      var msg = form.getAttribute && form.getAttribute('data-confirm');
      if (msg && !window.confirm(msg)) e.preventDefault();
    });
  }

  /* 4. Пароли: показать/скрыть, длина, совпадение */
  function initPasswords() {
    $all('input[type="password"]').forEach(function (input) {
      var wrap = document.createElement('div');
      wrap.className = 'password-wrap';
      input.parentNode.insertBefore(wrap, input);
      wrap.appendChild(input);
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'password-toggle';
      btn.setAttribute('aria-label', 'Показать пароль');
      btn.innerHTML = ICON_EYE;
      btn.addEventListener('click', function () {
        var hidden = input.type === 'password';
        input.type = hidden ? 'text' : 'password';
        btn.innerHTML = hidden ? ICON_EYE_OFF : ICON_EYE;
        btn.setAttribute('aria-label', hidden ? 'Скрыть пароль' : 'Показать пароль');
      });
      wrap.appendChild(btn);
    });

    var minInput = document.querySelector('[data-min-length]');
    if (minInput) {
      var minHint = document.getElementById(minInput.getAttribute('aria-describedby'));
      var min = parseInt(minInput.getAttribute('data-min-length'), 10);
      minInput.addEventListener('input', function () {
        if (!minHint) return;
        var len = minInput.value.length;
        minHint.classList.toggle('is-ok', len >= min);
        minHint.textContent = len >= min ? 'Длина подходит' : 'Минимум ' + min + ' символов · сейчас ' + len;
      });
    }

    $all('[data-match]').forEach(function (input) {
      var other = document.getElementById(input.getAttribute('data-match'));
      var hint = document.getElementById(input.getAttribute('aria-describedby'));
      if (!other || !hint) return;
      function check() {
        if (!input.value) { hint.textContent = ''; hint.className = 'hint'; return; }
        var ok = input.value === other.value;
        hint.textContent = ok ? 'Пароли совпадают' : 'Пароли не совпадают';
        hint.className = 'hint ' + (ok ? 'is-ok' : 'is-bad');
      }
      input.addEventListener('input', check);
      other.addEventListener('input', check);
    });
  }

  /* 5. Счётчик символов для комментария к записи (лимит 500 в форме) */
  function initCounters() {
    $all('textarea[name="comment"], textarea[data-max]').forEach(function (ta) {
      var max = parseInt(ta.getAttribute('data-max') || '500', 10);
      var out = document.createElement('div');
      out.className = 'field__counter';
      out.setAttribute('aria-live', 'polite');
      ta.insertAdjacentElement('afterend', out);
      function update() {
        var n = ta.value.length;
        out.textContent = n + ' / ' + max;
        out.classList.toggle('is-over', n > max);
      }
      ta.addEventListener('input', update);
      update();
    });
  }

  /* 6. Звёзды вместо select для оценки */
  function initStars() {
    var select = document.querySelector('select[name="rating"]');
    if (!select) return;
    var labels = ['', 'Плохо', 'Так себе', 'Нормально', 'Хорошо', 'Отлично'];
    var box = document.createElement('div');
    box.className = 'stars-input';
    box.setAttribute('role', 'radiogroup');
    box.setAttribute('aria-label', 'Оценка');
    var caption = document.createElement('span');
    caption.className = 'stars-input__label';
    var buttons = [];

    function paint(value) {
      buttons.forEach(function (b, i) {
        b.classList.toggle('is-on', i < value);
        b.setAttribute('aria-checked', String(i + 1 === Number(select.value)));
      });
      caption.textContent = labels[value] || 'Выберите оценку';
    }

    for (var i = 1; i <= 5; i++) {
      (function (v) {
        var b = document.createElement('button');
        b.type = 'button';
        b.setAttribute('role', 'radio');
        b.setAttribute('aria-label', v + ' из 5');
        b.innerHTML = ICON_STAR;
        b.addEventListener('click', function () { select.value = String(v); paint(v); });
        b.addEventListener('mouseenter', function () { paint(v); });
        b.addEventListener('focus', function () { paint(v); });
        buttons.push(b);
        box.appendChild(b);
      })(i);
    }
    box.addEventListener('mouseleave', function () { paint(Number(select.value) || 0); });
    box.addEventListener('keydown', function (e) {
      var cur = Number(select.value) || 0;
      if (e.key === 'ArrowRight' || e.key === 'ArrowUp') cur = Math.min(5, cur + 1);
      else if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') cur = Math.max(1, cur - 1);
      else return;
      e.preventDefault();
      select.value = String(cur);
      paint(cur);
      buttons[cur - 1].focus();
    });
    box.appendChild(caption);
    select.insertAdjacentElement('afterend', box);
    select.classList.add('visually-hidden');
    select.setAttribute('tabindex', '-1');
    paint(Number(select.value) || 0);
  }

  /* 7. Предпросмотр фото врача */
  function initPhotoPreview() {
    $all('input[type="file"]').forEach(function (input) {
      input.setAttribute('accept', 'image/*');
      input.addEventListener('change', function () {
        var file = input.files && input.files[0];
        var img = input.parentNode.querySelector('.photo-preview');
        if (!file) { if (img) img.remove(); return; }
        if (!img) {
          img = document.createElement('img');
          img.className = 'photo-preview';
          img.alt = 'Предпросмотр фото';
          input.insertAdjacentElement('afterend', img);
        }
        img.src = URL.createObjectURL(file);
      });
    });
  }

  /* 8. Подсказки для элементов с data-tip */
  function initTips() {
    var nodes = $all('[data-tip]');
    if (!nodes.length) return;
    var tip = document.createElement('div');
    tip.className = 'tip';
    tip.setAttribute('role', 'tooltip');
    document.body.appendChild(tip);
    function show(e) {
      var el = e.currentTarget;
      var r = el.getBoundingClientRect();
      tip.textContent = el.getAttribute('data-tip');
      tip.style.left = (r.left + r.width / 2) + 'px';
      tip.style.top = r.top + 'px';
      tip.classList.add('is-visible');
    }
    function hide() { tip.classList.remove('is-visible'); }
    nodes.forEach(function (n) {
      n.addEventListener('mouseenter', show);
      n.addEventListener('mouseleave', hide);
      n.addEventListener('focus', show);
      n.addEventListener('blur', hide);
    });
    window.addEventListener('scroll', hide, { passive: true });
  }

  /* 9. Поля с ошибками: aria-invalid + фокус на первую ошибку */
  function initFieldErrors() {
    var first = null;
    $all('.field.has-error').forEach(function (field) {
      var input = field.querySelector('input, select, textarea');
      if (input) {
        input.setAttribute('aria-invalid', 'true');
        if (!first) first = input;
      }
    });
    if (first) first.focus({ preventScroll: false });
  }

  /* 10. Цвет аватара-монограммы по имени */
  function initAvatars() {
    $all('.avatar[data-name]').forEach(function (a) {
      var s = a.getAttribute('data-name') || '';
      var h = 0;
      for (var i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) >>> 0;
      a.setAttribute('data-tone', String(h % 5));
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    initNav();
    initFlashes();
    initConfirm();
    initPasswords();
    initCounters();
    initStars();
    initPhotoPreview();
    initTips();
    initFieldErrors();
    initAvatars();
  });
})();
